import subprocess

arrbit = [2048, 4096, 8192]
choice = 0

while choice<1 or choice>3:
    choice = int(input('Pick a bit level 1=2048, 2=4096, 3=8192 (1,2,3):'))
bit=arrbit[choice]

days = int(input('How many DAYS valid for:'))
print("Enter above subjects.")
country = input('Country:')
state = input('State:')
city = input('City:')
ou = input('Organizational Unit:')
cn = input('CN:')

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

cmd2 = 'openssl req \
    -new \
    -subj "/C={country}/ST={state}/L={city}/O={ou}/CN={cn}" \
    -key {cn}.key \
    -out {cn}.csr'.format(country=country, state=state, city=city, ou=ou, cn=cn)
output = subprocess.check_output(['bash','-c', cmd2])

cmd3 = 'openssl x509 -req -days {days} -in {cn}.csr -CA {cn}.crt -CAkey {cn}.key -CAcreateserial -out {cn}-client.crt'.format(days=days, cn=cn)
output3 = subprocess.call(cmd3, shell=True)

cmd4 = 'openssl verify -CAfile {cn}.crt {cn}-client.crt'.format(cn=cn)
# output4 = subprocess.check_output(['bash','-c', cmd4])
result = subprocess.Popen(cmd4, shell = True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

output,res=result.communicate()
print (res)
