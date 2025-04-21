# Guía Definitiva de Comandos y Atajos en Kali Linux

## 🚀 Atajos de Teclado Fundamentales

### Gestión de Ventanas y Escritorio
- **Alt + Tab**: Cambiar entre ventanas abiertas
- **Alt + Shift + Tab**: Cambiar entre ventanas en orden inverso
- **Super (Tecla Windows) + D**: Mostrar/ocultar escritorio
- **Super + E**: Abrir gestor de archivos (Thunar)
- **Ctrl + Alt + T**: Abrir terminal
- **Super + Espacio**: Abrir menú de aplicaciones
- **Alt + F2**: Abrir cuadro de ejecución rápida
- **Super + L**: Bloquear pantalla

### Gestión de Terminales
- **Ctrl + Shift + T**: Abrir nueva pestaña en terminal
- **Ctrl + Shift + W**: Cerrar pestaña de terminal actual
- **Ctrl + Alt + T**: Abrir nueva ventana de terminal
- **Ctrl + Shift + C**: Copiar texto seleccionado
- **Ctrl + Shift + V**: Pegar texto copiado

## 🔒 Comandos Esenciales de Terminal

### Navegación y Gestión de Archivos
```bash
# Navegación básica
pwd         # Mostrar directorio actual
ls          # Listar archivos y directorios
cd /ruta    # Cambiar de directorio
cd ..       # Subir un nivel de directorio
cd ~        # Ir al directorio home
mkdir nombre    # Crear directorio
touch archivo   # Crear archivo vacío
cp origen destino   # Copiar archivos
mv origen destino   # Mover/renombrar archivos
rm archivo      # Eliminar archivo
rm -r directorio    # Eliminar directorio
```

### Permisos y Propietarios
```bash
# Cambiar permisos
chmod 755 archivo   # Cambiar permisos de archivo
chmod +x script.sh  # Hacer un archivo ejecutable
chown usuario:grupo archivo  # Cambiar propietario
```

### Información del Sistema
```bash
# Información del sistema
uname -a       # Detalles completos del sistema
whoami         # Usuario actual
df -h          # Uso de disco
free -h        # Memoria RAM
top            # Procesos en tiempo real
htop           # Version mejorada de top
```

### Gestión de Paquetes
```bash
# APT (Administrador de paquetes)
sudo apt update        # Actualizar lista de paquetes
sudo apt upgrade       # Actualizar sistema
sudo apt install paquete   # Instalar paquete
sudo apt remove paquete    # Desinstalar paquete
sudo apt autoremove    # Eliminar paquetes no necesarios
```

## 🕵️ Comandos de Seguridad y Hacking

### Herramientas de Red
```bash
# Análisis de red
ifconfig       # Configuración de interfaces de red
ip addr        # Mostrar direcciones IP
ping objetivo  # Probar conectividad
nmap objetivo  # Escaneo de puertos
wireshark      # Análisis de paquetes de red
```

### Herramientas de Seguridad
```bash
# Herramientas forenses y de seguridad
aircrack-ng       # Auditoría de redes WiFi
metasploit-framework  # Framework de penetración
john             # Crackeo de contraseñas
sqlmap           # Herramienta de inyección SQL
```

## 💻 Atajos de Terminal Avanzados

### Eficiencia en Comandos
- **!!**: Repetir último comando
- **!comando**: Repetir último comando que empieza con "comando"
- **Ctrl + R**: Buscar en historial de comandos
- **Ctrl + A**: Ir al inicio de la línea
- **Ctrl + E**: Ir al final de la línea
- **Ctrl + U**: Borrar línea actual
- **Ctrl + K**: Borrar desde el cursor hasta el final

### Redirección y Tuberías
```bash
# Ejemplos de redirección
comando > archivo        # Redirigir salida a archivo
comando >> archivo       # Agregar salida a archivo
comando1 | comando2      # Enviar salida de comando1 a comando2
```

## 🛡️ Consejos de Seguridad
- Siempre usar `sudo` con precaución
- Mantener el sistema actualizado
- Usar contraseñas robustas
- Configurar cortafuegos (ufw)

## 🚀 Personalización
- Bash Profile: `~/.bashrc`
- Alias personalizados: Agregar en `~/.bash_aliases`

### Ejemplo de Alias Útil
```bash
# En ~/.bash_aliases
alias update='sudo apt update && sudo apt upgrade -y'
alias ports='netstat -tuln'
```

## 📚 Recursos Adicionales
- Manual de comandos: `man comando`
- Ayuda rápida: `comando --help`

### Práctica Constante
La mejor forma de dominar Kali Linux es practicar regularmente. Experimenta, rompe y repara, ¡pero siempre en entornos controlados!