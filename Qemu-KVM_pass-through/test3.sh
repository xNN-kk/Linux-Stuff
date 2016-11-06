#!/bin/bash

cp /usr/share/edk2.git/ovmf-x64/OVMF_VARS-pure-efi.fd /tmp/my_vars.fd
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -cpu host,kvm=off \
  -vga none \
  -usb -usbdevice host:04ca:007d \
  -usb -usbdevice host:0461:4d17 \
  -device vfio-pci,host=04:00.0,multifunction=on \
  -device vfio-pci,host=04:00.1 \
  -drive if=pflash,format=raw,readonly,file=/usr/share/edk2.git/ovmf-x64/OVMF_CODE-pure-efi.fd \
  -drive if=pflash,format=raw,file=/tmp/my_vars.fd \
  -device virtio-scsi-pci,id=scsi \
  -drive file=/home/blackbyte/Desktop/vm2/win10.iso,id=isocd,format=raw,if=none -device scsi-cd,drive=isocd \
  -drive file=/home/blackbyte/Desktop/vm2/win.img,id=disk,format=qcow2,if=none,cache=writeback -device scsi-hd,drive=disk \
  -drive file=/home/blackbyte/Desktop/vm2/virt.iso,id=virtiocd,if=none,format=raw -device ide-cd,bus=ide.1,drive=virtiocd
