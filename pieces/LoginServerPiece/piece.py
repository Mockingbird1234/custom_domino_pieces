from .models import InputModel, OutputModel, AuthMethodType
from domino.base_piece import BasePiece
from pathlib import Path
import paramiko
import socket
import uuid
import time


class LoginPiece(BasePiece):
    
    # 类级别的连接池，用于存储SSH连接
    _connections = {}
    
    def piece_function(self, input_data: InputModel):
        
        try:
            # 创建SSH客户端
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 生成连接ID
            connection_id = str(uuid.uuid4())
            
            self.logger.info(f"Attempting to connect to {input_data.server_ip}:{input_data.port}")
            
            # 根据认证方法连接
            if input_data.auth_method == AuthMethodType.password:
                # 密码认证
                ssh_client.connect(
                    hostname=input_data.server_ip,
                    port=input_data.port,
                    username=input_data.username,
                    password=input_data.password,
                    timeout=input_data.connection_timeout
                )
            else:  # key认证
                # 密钥认证
                if not input_data.private_key_path or not Path(input_data.private_key_path).exists():
                    raise Exception("Private key file not found or not specified")
                
                ssh_client.connect(
                    hostname=input_data.server_ip,
                    port=input_data.port,
                    username=input_data.username,
                    key_filename=input_data.private_key_path,
                    timeout=input_data.connection_timeout
                )
            
            # 获取服务器信息
            try:
                # 获取主机名
                stdin, stdout, stderr = ssh_client.exec_command('hostname')
                hostname = stdout.read().decode().strip()
                
                # 获取操作系统信息
                stdin, stdout, stderr = ssh_client.exec_command('uname -a')
                os_info = stdout.read().decode().strip()
                
                # 如果uname失败，尝试其他命令
                if not os_info:
                    stdin, stdout, stderr = ssh_client.exec_command('cat /etc/os-release | head -1')
                    os_info = stdout.read().decode().strip()
                
            except Exception as e:
                self.logger.warning(f"Failed to get server info: {e}")
                hostname = input_data.server_ip
                os_info = "Unknown"
            
            # 存储连接到连接池
            self._connections[connection_id] = {
                'client': ssh_client,
                'server_ip': input_data.server_ip,
                'port': input_data.port,
                'username': input_data.username,
                'connected_at': time.time(),
                'hostname': hostname
            }
            
            server_info = f"{input_data.username}@{input_data.server_ip}:{input_data.port}"
            
            self.logger.info(f"Successfully connected to server: {server_info}")
            
            return OutputModel(
                login_success=True,
                connection_id=connection_id,
                server_info=server_info,
                server_hostname=hostname,
                server_os=os_info,
                base64_bytes_data=input_data.base64_bytes_data
            )
            
        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed - invalid credentials")
            return OutputModel(
                login_success=False,
                connection_id="",
                server_info="",
                server_hostname="",
                server_os="",
                base64_bytes_data=""
            )
        except paramiko.SSHException as e:
            self.logger.error(f"SSH connection error: {e}")
            return OutputModel(
                login_success=False,
                connection_id="",
                server_info="",
                server_hostname="",
                server_os="",
                base64_bytes_data=""
            )
        except socket.timeout:
            self.logger.error("Connection timeout")
            return OutputModel(
                login_success=False,
                connection_id="",
                server_info="",
                server_hostname="",
                server_os="",
                base64_bytes_data=""
            )
        except Exception as e:
            self.logger.error(f"Login error: {e}")
            return OutputModel(
                login_success=False,
                connection_id="",
                server_info="",
                server_hostname="",
                server_os="",
                base64_bytes_data=""
            )
    
    @classmethod
    def get_connection(cls, connection_id: str):
        """获取SSH连接"""
        return cls._connections.get(connection_id)
    
    @classmethod
    def close_connection(cls, connection_id: str):
        """关闭SSH连接"""
        if connection_id in cls._connections:
            try:
                cls._connections[connection_id]['client'].close()
            except:
                pass
            del cls._connections[connection_id]