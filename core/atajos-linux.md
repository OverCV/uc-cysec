# Guía Definitiva de Redes en Kali Linux

## 🌐 Información de Red Fundamental

### Identificación de Interfaces de Red
La primera herramienta que necesitarás para entender tu configuración de red es identificar tus interfaces de red. Existen varios comandos para esto:

```bash
# Método 1: Mostrar todas las interfaces de red
ip addr show

# Método 2: Otra forma clásica de mostrar interfaces
ifconfig

# Método 3: Información detallada de interfaces
ip link show
```

### Obtener Dirección IP

```bash
# Mostrar IP privada
hostname -I

# Mostrar IP pública (requiere conexión a internet)
curl ifconfig.me

# Otra forma de ver IP pública
wget -qO- ifconfig.me
```

## 🔍 Escaneo y Descubrimiento de Redes

### Escaneo de Red Local
```bash
# Escaneo de red local con ARP
sudo arp-scan -I eth0 --localnet

# Escaneo de red con Nmap (descubrimiento de hosts)
sudo nmap -sn 192.168.1.0/24

# Escaneo de puertos abiertos en la red
sudo nmap -sT 192.168.1.0/24
```

### Información de Conectividad
```bash
# Ping básico (prueba de conectividad)
ping google.com

# Ping con número específico de paquetes
ping -c 4 google.com

# Traza de ruta para ver saltos de red
traceroute google.com

# Versión alternativa de traza de ruta
tracepath google.com
```

## 🛠️ Herramientas de Diagnóstico de Red

### Información de Conexiones
```bash
# Mostrar conexiones de red activas
netstat -tuln

# Conexiones establecidas
netstat -ano

# Ver puertos abiertos con ss (más moderno que netstat)
ss -tuln
```

### Resolución de Nombres
```bash
# Información de servidores DNS
cat /etc/resolv.conf

# Consultas DNS
nslookup google.com

# Otra herramienta de consulta DNS
dig google.com
```

## 🌍 Información Detallada de Red

### Información de Enrutamiento
```bash
# Tabla de enrutamiento
route -n

# Otra forma de ver rutas
ip route show
```

### Configuración de Red
```bash
# Información completa de interfaces
ip addr

# Configurar manualmente una interfaz
sudo ip addr add 192.168.1.100/24 dev eth0

# Levantar/bajar una interfaz de red
sudo ip link set eth0 up
sudo ip link set eth0 down
```

## 🕵️ Herramientas Avanzadas de Red

### Captura de Paquetes
```bash
# Captura básica con tcpdump
sudo tcpdump -i eth0

# Captura de paquetes guardando en archivo
sudo tcpdump -i eth0 -w captura.pcap

# Captura con Wireshark (interfaz gráfica)
wireshark
```

### Análisis de Puertos
```bash
# Escaneo de puertos específicos
nmap -p 80,443,22 192.168.1.1

# Escaneo de todos los puertos
nmap -p- 192.168.1.1

# Escaneo con detección de versiones
nmap -sV 192.168.1.1
```

## 🔒 Consejos de Seguridad en Redes

1. **Siempre usar `sudo`** para comandos que requieren privilegios de administrador.
2. **Ser cauteloso** al usar herramientas de escaneo en redes que no son tuyas.
3. **Entender el impacto** de los comandos antes de ejecutarlos.
4. **Proteger tu información de red**.

### Configuración de Firewall
```bash
# Verificar estado del firewall
sudo ufw status

# Habilitar firewall
sudo ufw enable

# Permitir un puerto específico
sudo ufw allow 22/tcp
```

## 📚 Recursos de Aprendizaje

- **Práctica constante**: La mejor forma de aprender es experimentando.
- **Documentación**: Consultar `man` de cada comando.
- **Entornos seguros**: Practica en máquinas virtuales o redes controladas.

### Ejemplo de Flujo de Trabajo
1. Identificar interfaces: `ip addr`
2. Verificar conectividad: `ping google.com`
3. Escanear red local: `sudo nmap -sn 192.168.1.0/24`
4. Analizar puertos abiertos: `sudo nmap -sT 192.168.1.0/24`

## 🚨 Advertencia Final
Recuerda que muchos de estos comandos pueden ser invasivos. **Nunca los uses en redes o sistemas sin autorización explícita**. La ética y el respeto son fundamentales en la seguridad informática.