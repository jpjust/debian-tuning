#!/usr/bin/env python3

import subprocess
import sys

NOUVEAU_BLACKLIST = '/etc/modprobe.d/nouveau-blacklist.conf'
NVIDIA_CONF = '/etc/modprobe.d/nvidia.conf'

def _help():
  print('Use:\n')
  print(f'{sys.argv[0]} 1\tHabilita NVidia proprietário')
  print(f'{sys.argv[0]} 0\tHabilita driver nouveau')

def _set_proprietary():
  try:
    nouveau_blacklist = open(NOUVEAU_BLACKLIST, 'w')
    nouveau_blacklist.write('blacklist nouveau\n')
    nouveau_blacklist.write('options nouveau modeset=0\n')
    nouveau_blacklist.close()

    nvidia_conf = open(NVIDIA_CONF, 'w')
    nvidia_conf.write('options nvidia-drm modeset=1\n')
    nvidia_conf.write('options nvidia-drm fbdev=1\n')
    nvidia_conf.close()

    res = subprocess.run(['update-initramfs', '-u'])
    if res.returncode == 0:
      print('Feito! Você agora está com a configuração para o driver proprietário da NVidia. Reinicie o computador.')
    else:
      print('Os arquivos de configuração foram ajustados, mas houve um erro ao executar \"update-initramfs -u\". Tente executar manualmente.')
  except PermissionError:
    print('Você não tem permissão para alterar arquivos do sistema. Execute como root.')

def _set_nouveau():
  try:
    nouveau_blacklist = open(NOUVEAU_BLACKLIST, 'w')
    nouveau_blacklist.write('')
    nouveau_blacklist.close()

    nvidia_conf = open(NVIDIA_CONF, 'w')
    nvidia_conf.write('')
    nvidia_conf.close()

    res = subprocess.run(['update-initramfs', '-u'])
    if res.returncode == 0:
      print('Feito! Você agora está com a configuração para o driver nouveau. Reinicie o computador.')
    else:
      print('Os arquivos de configuração foram ajustados, mas houve um erro ao executar \"update-initramfs -u\". Tente executar manualmente.')
  except PermissionError:
    print('Você não tem permissão para alterar arquivos do sistema. Execute como root.')

if len(sys.argv) != 2:
  _help()
  exit()

if sys.argv[1] == '1':
  _set_proprietary()
elif sys.argv[1] == '0':
  _set_nouveau()
else:
  _help()
