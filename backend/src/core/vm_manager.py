import os
import random
import subprocess
import socket
import libvirt
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring 

#укажите любой раздел, где достаточно места
PATH_VMS = '/home/VMConnect/VMs/'
class VMManager:
    def __init__(self, uri="qemu:///system"):
        self.conn = libvirt.open(uri)
        if not self.conn:
            raise Exception("Failed to open connection to the hypervisor")

    def create_disk(self, vm_name, disk_size_gb=10):
        """Создает диск для виртуальной машины.
        Можете указать любой путь до раздела с нужным свободным местом"""
        disk_path = f"{PATH_VMS}{vm_name}.qcow2"
        if not os.path.exists(disk_path):
            subprocess.run(
                ["qemu-img", "create", "-f", "qcow2", "-o", "preallocation=full", disk_path, f"{disk_size_gb}G"],
                check=True
            )
        return disk_path
    '''Укажите расположение ISO'''
    def create_vm(self, vm_name, memory_mb=1024, vcpu_count=1, disk_size_gb=10, 
              iso_path='/var/lib/libvirt/iso/ubuntu-24.10-desktop-amd64.iso', 
              vnc_password='123456'):  # Добавляем параметр для пароля VNC
        """Создает виртуальную машину с загрузкой с ISO-образа (CD-ROM) на vdb/scsi."""
        # Проверяем, существует ли уже такая виртуальная машина
        try:
            existing_vm = self.conn.lookupByName(vm_name)
            if existing_vm:
                raise Exception(f"VM with name {vm_name} already exists")
        except libvirt.libvirtError as e:
            if "no domain with matching name" not in str(e):
                raise e  # Перебрасываем другие ошибки libvirt

        # Создаем диск для виртуальной машины
        disk_path = self.create_disk(vm_name, disk_size_gb)

        # Создаем XML-конфигурацию для виртуальной машины
        domain = Element('domain', type='kvm')
        name = SubElement(domain, 'name')
        name.text = vm_name

        memory = SubElement(domain, 'memory', unit='KiB')
        memory.text = str(memory_mb * 1024)

        vcpu = SubElement(domain, 'vcpu')
        vcpu.text = str(vcpu_count)

        os_element = SubElement(domain, 'os')
        type_element = SubElement(os_element, 'type', arch='x86_64')
        type_element.text = 'hvm'

        # Настройка загрузки с CD-ROM
        boot_cdrom = SubElement(os_element, 'boot', dev='cdrom')  # Приоритет загрузки с CD-ROM
        boot_hd = SubElement(os_element, 'boot', dev='hd')        # Загрузка с жесткого диска

        features = SubElement(domain, 'features')
        acpi = SubElement(features, 'acpi')
        apic = SubElement(features, 'apic')

        clock = SubElement(domain, 'clock', offset='utc')

        on_poweroff = SubElement(domain, 'on_poweroff')
        on_poweroff.text = 'destroy'

        on_reboot = SubElement(domain, 'on_reboot')
        on_reboot.text = 'restart'

        on_crash = SubElement(domain, 'on_crash')
        on_crash.text = 'destroy'

        devices = SubElement(domain, 'devices')

        # Добавляем диск
        disk_device = SubElement(devices, 'disk', type='file', device='disk')
        source = SubElement(disk_device, 'source', file=disk_path)
        target = SubElement(disk_device, 'target', dev='vda')

        # Добавляем CD-ROM (ISO-образ) на vdb/scsi
        if iso_path:
            cdrom_device = SubElement(devices, 'disk', type='file', device='cdrom', bootOrder="1")  # Приоритет загрузки
            driver = SubElement(cdrom_device, 'driver', name='qemu', type='raw')
            cdrom_source = SubElement(cdrom_device, 'source', file=iso_path)
            cdrom_target = SubElement(cdrom_device, 'target', dev='vdb', bus='scsi')
            cdrom_readonly = SubElement(cdrom_device, 'readonly')

        # Добавляем сетевой интерфейс
        interface = SubElement(devices, 'interface', type='network')
        source_network = SubElement(interface, 'source', network='default')

        # Добавляем графический интерфейс VNC с возможностью задать пароль
        graphics = SubElement(devices, 'graphics', type='vnc', port='-1', autoport='yes', listen='127.0.0.1', passwd=vnc_password)
        
        SubElement(graphics, 'listen', type='address', address='127.0.0.1')

        # Добавляем клавиатуру
        keyboard = SubElement(devices, 'input', type='keyboard', bus='usb')

        # Преобразуем XML в строку
        xml_config = tostring(domain).decode()

        # Определяем и запускаем виртуальную машину
        try:
            self.conn.defineXML(xml_config)
            vm = self.conn.lookupByName(vm_name)
            vm.create()

            # Получаем назначенный VNC-порт
            updated_xml = vm.XMLDesc(0)
            domain = ET.fromstring(updated_xml)
            vnc_port = domain.find('.//graphics[@type="vnc"]').get('port')

            # Запускаем noVNC
            novnc_port = self._get_unique_novnc_port()  # Генерируем уникальный порт для noVNC
            command = ['websockify', str(novnc_port), f'0.0.0.0:{vnc_port}', '--web', '/usr/share/novnc/' ]
            try:
                subprocess.Popen(command)
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при старте noVNC: {e}")

            return {
                "message": "VM created successfully",
                "vm_name": vm_name,
                "novnc_port": novnc_port,
                "vnc_port": vnc_port
            }
        except Exception as e:
            raise Exception(f"Failed to create VM: {str(e)}")
    
    def change_vnc_password(self, vm_name, new_password):
        """
        Изменяет пароль VNC для уже созданной виртуальной машины.

        :param vm_name: Имя виртуальной машины.
        :param new_password: Новый пароль VNC.
        :return: Сообщение об успешном изменении пароля.
        """
        try:
            # Получаем объект виртуальной машины
            vm = self.conn.lookupByName(vm_name)
            if not vm:
                raise Exception(f"VM with name {vm_name} does not exist")

            # Получаем текущую XML-конфигурацию виртуальной машины
            xml_config = vm.XMLDesc(0)

            # Парсим XML-конфигурацию
            domain = ET.fromstring(xml_config)

            # Находим секцию <graphics> для VNC
            graphics = domain.find(".//devices/graphics[@type='vnc']")
            if graphics is None:
                raise Exception("VNC graphics configuration not found in the VM's XML")

            # Изменяем пароль VNC
            graphics.set('passwd', new_password)

            # Преобразуем обновленное XML обратно в строку
            updated_xml = ET.tostring(domain, encoding='unicode')

            # Обновляем конфигурацию виртуальной машины
            vm.undefine()  # Удаляем текущее определение ВМ (без удаления данных)
            self.conn.defineXML(updated_xml)  # Определяем ВМ с новой конфигурацией

            return {"message": "VNC password changed successfully", "vm_name": vm_name}

        except libvirt.libvirtError as e:
            raise Exception(f"Libvirt error while changing VNC password: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to change VNC password: {str(e)}")

    def _get_unique_novnc_port(self):
        """Генерирует уникальный порт для noVNC."""
        base_port = 6080
        max_retries = 100
        for _ in range(max_retries):
            port = random.randint(base_port, base_port + 1000)
            if self._is_port_available(port):
                return port
        raise Exception("No available noVNC ports found")

    def _is_port_available(self, port):
        """Проверяет, занят ли порт."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) != 0
    
    #Запуск виртуальной машины
    def start_vm(self, vm_name):
        """Запускает виртуальную машину по имени."""
        try:
            vm = self.conn.lookupByName(vm_name)
            if vm.isActive():
                return {"message": f"VM {vm_name} is already running."}
            vm.create()
            return {"message": f"VM {vm_name} started successfully."}
        except libvirt.libvirtError as e:
            raise Exception(f"Failed to start VM {vm_name}: {str(e)}")
    
    def stop_vm(self, vm_name):
        """Останавливает виртуальную машину по имени."""
        try:
            vm = self.conn.lookupByName(vm_name)
            if not vm.isActive():
                return {"message": f"VM {vm_name} is already stopped."}
            vm.destroy()
            return {"message": f"VM {vm_name} stopped successfully."}
        except libvirt.libvirtError as e:
            raise Exception(f"Failed to stop VM {vm_name}: {str(e)}")

    
    def detach_iso(self, vm_name):
        """Отключает ISO-образ (CD-ROM) от виртуальной машины."""
        try:
            # Находим виртуальную машину по имени
            vm = self.conn.lookupByName(vm_name)
            if not vm:
                raise Exception(f"VM with name {vm_name} not found")

            # Получаем текущую XML-конфигурацию виртуальной машины
            xml_config = vm.XMLDesc(0)
            domain = ET.fromstring(xml_config)

            # Находим и удаляем секцию CD-ROM
            for disk in domain.findall('devices/disk'):
                if disk.get('device') == 'cdrom':
                    domain.find('devices').remove(disk)

            # Обновляем XML-конфигурацию без CD-ROM
            new_xml_config = ET.tostring(domain).decode()

            # Применяем обновленную конфигурацию
            vm.destroy()  # Останавливаем машину (если она активна)
            vm.undefine()  # Удаляем старое определение
            self.conn.defineXML(new_xml_config)  # Создаем новое определение
            vm.start() #снова запускаем виртуальную машину
            return {"message": f"ISO image detached from VM {vm_name}"}

        except libvirt.libvirtError as e:
            raise Exception(f"Failed to detach ISO: {str(e)}")
    
    def hot_detach_iso(self, vm_name):
        """Горячее отключение ISO-образа (CD-ROM) без перезапуска ВМ."""
        try:
            # Находим виртуальную машину по имени
            vm = self.conn.lookupByName(vm_name)
            if not vm:
                raise Exception(f"VM with name {vm_name} not found")

            if not vm.isActive():
                raise Exception(f"VM {vm_name} is not running. Hot-unplug is not possible.")

            # Получаем текущую XML-конфигурацию виртуальной машины
            xml_config = vm.XMLDesc(0)
            domain = ET.fromstring(xml_config)

            # Находим секцию CD-ROM
            for disk in domain.findall('devices/disk'):
                if disk.get('device') == 'cdrom':
                    cdrom_xml = ET.tostring(disk, encoding='unicode')
                    vm.detachDevice(cdrom_xml)  # Горячее отключение CD-ROM
                    return {"message": f"ISO image hot-detached from VM {vm_name}"}

            raise Exception("CD-ROM device not found in VM configuration")

        except libvirt.libvirtError as e:
            raise Exception(f"Failed to hot-detach ISO: {str(e)}")

    def delete_vm(self, vm_name):
        """Удаляет виртуальную машину."""
        try:
            vm = self.conn.lookupByName(vm_name)
            if vm.isActive():
                vm.destroy()  # Останавливаем машину, если она активна
            vm.undefine()  # Удаляем определение машины
            disk_path = f"{PATH_VMS}{vm_name}.qcow2"
            if os.path.exists(disk_path):
                os.remove(disk_path)
            return {"message": "VM deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete VM: {str(e)}")
    def list_active_vm(self):
        names_vm = []
        '''Получает список активных виртуальных машин'''
        try:
            # Подключаемся к локальному гипервизору (QEMU/KVM)
            self.conn = libvirt.open("qemu:///system")
            if self.conn is None:
                print("Не удалось подключиться к libvirt")
                exit(1)
            active_domains_ids = self.conn.listDomainsID()
            for domain_id in active_domains_ids:
                domain = self.conn.lookupByID(domain_id)
                names_vm.append(domain.name)
            # Закрытие соединения
            self.conn.close()
            return names_vm
        except libvirt.libvirtError as e:
            print(f"Ошибка libvirt: {e}")
    def list_inactive_vm(self):
        '''Получает список активных и неактивных виртуальных машин'''
        names_vm = []
        try:
            # Подключаемся к локальному гипервизору (QEMU/KVM)
            self.conn = libvirt.open("qemu:///system")
            if self.conn is None:
                print("Не удалось подключиться к libvirt.")
                exit(1)
            #Получение списка неактивных доменов
            inactive_domains_names = self.conn.listDefinedDomains()
            for domain_name in inactive_domains_names:
                names_vm.append(domain_name)
            # Закрытие соединения
            self.conn.close()
            return names_vm

        except libvirt.libvirtError as e:
            print(f"Ошибка libvirt: {e}")
    
        
        
        