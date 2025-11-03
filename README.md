## Inicialização

Opções recomendadas em `/etc/default/grub`:

```
GRUB_CMDLINE_LINUX_DEFAULT="nouveau.nomodeset nvidia_drm.modeset=1 fsck.mode=auto fsck.repair=yes splash"
```

* `nouveau.nomodeset`: Desativa driver nouveau (se usar Nvidia proprietário)
* `nvidia_drm.modeset=1`: Ativa o driver proprietario da Nvidia
* `fsck.mode=auto`: fsck automático em caso de partição suja
* `fsck.repair=yes`: fsck repara automaticamente qualquer erro
* `splash`: Exibe tela de splash

É preciso atualizar o Grub após alterar a configuração:

```sh
update-grub
```

## Tuning de acesso ao disco

Adicione `noatime,nodiratime` nas opções das partições ext4 em `/etc/fstab` para evitar gravar tempo de acesso (aumenta o desempenho e poupa escritas em SSDs).

Adicione pontos de montagem de diretórios temporários na memória RAM:

```
# Temporarios
tmpfs   /tmp       tmpfs   defaults,noatime,nodiratime,mode=1777   0  0
tmpfs   /var/tmp   tmpfs   defaults,noatime,nodiratime,mode=1777   0  0
```

## Tuning de SSD

Ative TRIM semanal:

```sh
systemctl enable --now fstrim.timer
systemctl list-timers
```

Desative journal nas partições ext4 (a partição não pode estar montada):

```sh
tune2fs -O ^has_journal /dev/sda2
```

## Rotacionamento dos logs do journald

Edite o arquivo `/etc/systemd/journald.conf` e adicione ou descomente a linha a seguir:

```conf
MaxRetentionSec=7day
```

Esta configuração limita os logs a 7 dias. É possível também configurar por tamanho. Veja os exemplos a seguir:

```conf
SystemMaxUse=200M
SystemKeepFree=50M
SystemMaxFileSize=50M
MaxRetentionSec=1month
```

Decida sua configuração e reinicie o `journald`:

```sh
systemctl restart systemd-journald
```

## Splash na inicialização com Plymouth

```sh
apt install plymouth*
```

Configuração em `/etc/plymouth/plymouthd.conf`:

```
[Daemon]
Theme=bgrt
ShowDelay=0
```

É preciso atualizar o initramfs após alterar a configuração:

```sh
update-initramfs -u
```

## Som com ruídos no Debian 13

O PipeWire do Debian 13 pode apresentar ruídos em alguns casos. A solução é copiar a configuração global do sistema para a pasta do usuário e alterar uma opção:

```sh
mkdir -p ~/.config/pipewire
cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire
```

Edite o o arquivo copiado e descomente a linha abaixo:

```
clock.power-of-two-quantum = true
```

Em seguida reinicie o PipeWire:

```sh
systemctl --user restart wireplumber pipewire pipewire-pulse
```

## Habilitando o Wayland no GNOME mesmo com driver proprietário Nvidia

Não é recomendado, pois ainda há instabilidade com Wayland+Nvidia, porém resolve o bug de travar após suspensão quando remove algum dispositivo USB.

Primeiro é preciso ter o mutter instalado:

```sh
apt install mutter
```

Edite `/etc/gdm3/daemon.conf` e ative o Wayland com a opção abaixo:

```
[daemon]
WaylandEnable=true
```

## Extensões que uso no GNOME Shell

* `gnome-shell-extension-appindicator`: Exibe ícones de bandeija na barra superior.
* `gnome-shell-extension-dashtodock`: Transforma o Dash do GNOME Shell em um dock.
* `gnome-shell-extension-freon`: Exibe temperaturas de dispositivos na barra superior.

## Uso do avahi para resolver nomes .local

Edite `/etc/nsswitch.conf` e adicione `mdns_minimal` na lista de busca:

```
hosts:          files mdns_minimal [NOTFOUND=return] dns myhostname mymachines
```
