import win32com.client
import uuid

mac_address: int = uuid.getnode()
formatted_mac_addr: str = ':'.join(['{:02x}'.format((uuid.getnode() >> e) & 0xff) for e in range(0, 8 * 6, 8)][::-1])
print(f'The MAC address is {formatted_mac_addr}')

objWMIService = win32com.client.Dispatch('WbemScripting.SWbemLocator')
objSWbemServices = objWMIService.ConnectServer('.', 'root\cimv2')
colItems = objSWbemServices.ExecQuery("Select * from Win32_Share")

print('\nAll shared resources:')

for objItem in colItems:
    print(f"{'-' * 30}\nAccess Mask: {objItem.AccessMask}\nAllow Maximum: {objItem.AllowMaximum}\n"
          f"Allow Maximum: {objItem.AllowMaximum}\nCaption: {objItem.Caption}\nDescription: {objItem.Description}\n"
          f"Install Date: {objItem.InstallDate}\nMaximum Allowed: {objItem.MaximumAllowed}\n"
          f"Name: {objItem.Name}\nPath: {objItem.Path}\nStatus: {objItem.Status}\nType: {objItem.Type}")
