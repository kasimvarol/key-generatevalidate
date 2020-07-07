import subprocess

def create_key(bit, days, country, state, city, ou, cn):
    cmd1 = 'openssl req \
        -new \
        -newkey rsa:{bit} \
        -days {days} \
        -nodes \
        -x509 \
        -subj "/C={country}/ST={state}/L={city}/O={ou}/CN={cn}" \
        -keyout {cn}.key \
        -out {cn}.crt'.format(bit=bit, days=days, country=country, state=state, city=city, ou=ou, cn=cn)
    output = subprocess.check_output(['bash','-c', cmd1])

def create_crt(country, state, city, ou, cn):
    cmd2 = 'openssl req \
        -new \
        -subj "/C={country}/ST={state}/L={city}/O={ou}/CN={cn}" \
        -key {cn}.key \
        -out {cn}.csr'.format(country=country, state=state, city=city, ou=ou, cn=cn)
    output = subprocess.check_output(['bash','-c', cmd2])

def create_client_crt(days, cn):
    cmd3 = 'openssl x509 -req -days {days} -in {cn}.csr -CA {cn}.crt -CAkey {cn}.key -CAcreateserial -out {cn}-client.crt'.format(days=days, cn=cn)
    output3 = subprocess.call(cmd3, shell=True)

def verify_crt(cn):
    cmd4 = 'openssl verify -CAfile {cn}.crt {cn}-client.crt'.format(cn=cn)
    # output4 = subprocess.check_output(['bash','-c', cmd4])
    result = subprocess.Popen(cmd4, shell = True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    dummy,res=result.communicate()
    print (res)

def pfx_to_crt(cn):
    cmd5 = 'openssl pkcs12 -export -out {cn}.pfx -inkey {cn}.key -in {cn}.crt'.format(cn=cn)
    li = list(cmd5.split(" ")) 
    subprocess.run(li)

def check_crt(cert):
    with open(cert, "r") as f:
        first = f.readline()
        for last in f: pass

    beg = "-----BEGIN CERTIFICATE-----\n"
    end = "-----END CERTIFICATE-----\n"


    if beg==first and last==end:
        print("Certification struct looks okay.")
    else:
        print("It is invalid.")

