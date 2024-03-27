from netmiko import ConnectHandler

def validate_ip_address(ip_string):
    parts = ip_string.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True

       
def validate_ip_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if not validate_ip_address(line):
                        return False
        return True
    except FileNotFoundError:
        print("Fisierul nu a fost gasit.")
        return False

def validate_conf_file(file):
    try:
        with open(file, 'r') as f: 
            first_line = f.readline().strip()
            if not first_line == "conf t":
                return False 
        return True
    
    except FileNotFoundError:
        print("Fisierul nu a fost gasit.")
        return False



filename = input("Introduceti numele fisierului: ")

if validate_ip_file(filename):
    print("Fisierul contine doar adrese IPv4 valide.")
else:
    print("Fisierul contine cel putin o adresă nevalida sau alt text.")
    exit()

def extract_configuration(filename):
    print("Opțiunea 1: Extragerea configuratiei")
    with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                cisco_ios_v = {
                    'device_type': 'cisco_ios',
                    'host':  line,
                    'username': 'admin',
                    'password': 'cisco',
                    'secret': 'cisco',
                    }
                session = ConnectHandler(**cisco_ios_v)
                
                conf = session.send_command('show run')

                l = conf.split('\n')

                for x in l:
                    if "hostname" in x:
                        index = x.index("hostname") + len("hostname") + 1

                        hostname = x[index:]
                        with open(hostname+'.txt', "a") as output:
                            for word in l :
                                output.write(word + '\n')
                        print("Configuratia de pe " + hostname + " a fost extrasa")        

                session.disconnect()
    

def aplicare(filename):
    print("Optiunea 2: Aplicarea configuratiei")
    filea = input("Introduceti numele fisierului de configurare: ")

    if validate_conf_file(filea) == True :
        with open(filename, 'r') as file:

                lines = file.readlines()
                for line in lines:
                    cisco_ios_v = {
                        'device_type': 'cisco_ios',
                        'host':  line,
                        'username': 'admin',
                        'password': 'cisco',
                        'secret': 'cisco',
                        }
                    session = ConnectHandler(**cisco_ios_v)

                    with open(filea, 'r') as file1:

                        comenzi = file1.readlines()
                        for com in comenzi:
                            session.write_channel(com)
                            print("A fost efectuata comanda " + com)

                session.disconnect()
    else :
         print ("Fisierul nu este valid!")

def verificare(filename):
    with open(filename, 'r') as file:

                lines = file.readlines()
                for line in lines:
                    cisco_ios_v = {
                        'device_type': 'cisco_ios',
                        'host':  line,
                        'username': 'admin',
                        'password': 'cisco',
                        'secret': 'cisco',
                        }
                    session = ConnectHandler(**cisco_ios_v)

                    for x in lines:
                        print("Incercare ping de la " + line + " pana la " + x )
                        print(session.send_command('ping ' + x))

                    session.disconnect()    

def diferente(filename): 

    with open(filename, 'r') as file:

        lines = file.readlines()
        ip1 = lines[0]
        ip2 = lines[1]
        
        cisco_ios_v1 = {
            'device_type': 'cisco_ios',
            'host':  ip1,
            'username': 'admin',
            'password': 'cisco',
            'secret': 'cisco',
            }
        session1 = ConnectHandler(**cisco_ios_v1)

        cisco_ios_v2 = {
            'device_type': 'cisco_ios',
            'host':  ip2,
            'username': 'admin',
            'password': 'cisco',
            'secret': 'cisco',
            }
        session2 = ConnectHandler(**cisco_ios_v2)

        conf1 = (session1.send_command('show run')).split('\n')
        conf2 = (session2.send_command('show run')).split('\n')

        set1 = set(conf1)
        set2 = set(conf2)

        d = str(set1.symmetric_difference(set2)).split('\n')
        for x in d:
            print(x + '\n')

        session1.disconnect() 
        session2.disconnect() 
    


def op3(filename):
    
    while True:

        print("\nSubmeniu:")
        print("1. Verificarea conectivitatii (ping)")
        print("2. Extragerea diferentelor dintre doua configuratii")
        print("0. Iesire")

        choice = input("Introduceti optiunea: ")

        if choice == "1":
            verificare(filename)
        elif choice == "2":
            diferente(filename)
        elif choice == "0":
            print("Iesire din program.")
            break
        else:
            print("Optiune invalida. Alegeti din nou.")
        
                     

    

while True:
    print("\nMeniu:")
    print("1. Extragerea configuratiei")
    print("2. Aplicarea configuratiei")
    print("3. A treia optiune")
    print("0. Iesire")

    choice = input("Introduceti optiunea: ")

    if choice == "1":
        extract_configuration(filename)
    elif choice == "2":
        aplicare(filename)
    elif choice == "3":
        op3(filename)
    elif choice == "0":
        print("Iesire din program.")
        break
    else:
        print("Optiune invalida. Alegeti din nou.")
  


