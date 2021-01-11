from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from pprint import pprint
from scrapli.driver.core import IOSXEDriver
import colorama
from colorama import Fore, Style
import ipdb
from nornir_scrapli.tasks import (
    get_prompt,
    send_command,
    send_configs
)

nr = InitNornir(config_file="config.yaml")
ted_targets=nr.filter(F(campus='ted'))
mar_targets=nr.filter(F(campus='mar'))
tedresultt = ted_targets.run(task=send_command, command="show running-config | inc dns-server")
marresultt = mar_targets.run(task=send_command, command="show running-config | inc dns-server")
def ted_campus():
    result = ted_targets.run(task=send_command, command="show running-config | inc ip dhcp pool")
    for y in result.keys():
      for x in result:
        temp=result[x][0].result
        temp2=temp.splitlines()
        print(temp2)
        if 'ip dhcp pool' in temp:
             print_result('yes')
             for x in temp2:
                 print(x)
                 commands=[x ,'dns-server x.x.x.x x.x.x.x x.x.x.x']
                 ted_targets.run(task=send_configs,configs=commands)
                 print('-'*80)
                 print(Fore.GREEN + 'yes dns added for ', y)
                 print('-'*80)
        else:
               print('dhcp pool found not found')
def mar_campus():
    result2 = mar_targets.run(task=send_command, command="show running-config | inc ip dhcp pool")
    for y in result2.keys():
      for x in result2:
        temp=result2[x][0].result
        temp2=temp.splitlines()
        print(temp2)
      if 'ip dhcp pool' in temp:
             print_result('yes')
             for z in temp2:
                print(z)
                commands=[z ,'dns-server x.x.x.x x.x.x.x x.x.x.x']
                mar_targets.run(task=send_configs,configs=commands)
                print('-'*80)
                print(Fore.GREEN +'yes dns added for ', y)
                print('-'*80)
      else:
              print('no')
def dnscheck():
            print('-'*80)
            teddns=ted_targets.run(task=send_command,configs='show running-config | inc dns-server ')
            for x in tedresultt:
              teddns1=tedresultt[x][0].result
            print(Fore.CYAN + '-'*30 + 'DNS RESULT' + Fore.CYAN + '-'*30)
            print(Fore.RED + teddns1)
            print(Fore.CYAN + '-'*80)
            print(Fore.CYAN + '-'*30 + 'DNS RESULT' + Fore.CYAN + '-'*30)
            for x in marresultt:
               mardns1=marresultt[x][0].result
            print(Fore.RED + mardns1)
            print('-'*80)
def main():
    ted_campus()
    mar_campus()
    dnscheck()
if __name__ == '__main__':
    main()



#ipdb.set_trace()
