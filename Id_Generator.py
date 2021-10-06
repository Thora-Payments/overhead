from Id_Class import Id
from Helper_Functions import Gen_Secret


rand = Gen_Secret()
Id_Sender0 = Id(rand)
print("Secret Seed for Sender 0: " + rand)
print("Address of Sender 0: " + Id_Sender0.addr)

rand = Gen_Secret()
Id_Sender1 = Id(rand)
print("Secret Key of Sender 1: " + rand)
print("Address of Sender 1: " + Id_Sender1.addr)

rand = Gen_Secret()
Id_Receiver0 = Id(rand)
print("Secret Key of Receiver 0: " + rand)
print("Address of Receiver 0: " + Id_Receiver0.addr)

rand = Gen_Secret()
Id_Receiver1 = Id(rand)
print("Secret Key of Receiver 1: " + rand)
print("Address of Receiver 1: " + Id_Receiver1.addr)


