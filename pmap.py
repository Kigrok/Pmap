import socket, requests, json, argparse, multiprocessing
from datetime import datetime
from pyfiglet import Figlet

def get_args():

	parser = argparse.ArgumentParser()

	parser.add_argument('-u', '--url', 
		dest = 'url', 
		help = 'URL / IP')

	parser.add_argument('-p', '--port', 
		dest = 'port', 
		help = 'Ports range.\nFormat: 8080 or (80-8080) or (80/8080) or (21,80,443,...)')

	parser.add_argument('-t', '--threads', 
		dest = 'threads', 
		help = 'Number of threads')

	options = parser.parse_args()
	return options


# Get website's location info
def info(ip):

	''' Output website's country, sity and timezone '''

	try:
		response = requests.get(f'http://ip-api.com/json/{ip}').json()
		return response['country'], response['city'], response['timezone'], response['countryCode']

	except Exception as e:
		return '\033[31mConnection Error\033[00m', '\033[31mN/A\033[00m', '\033[31mN/A\033[00m', '\033[31mN/A\033[00m'


# Banner
def banner(name, ip):

	''' Output banner and ip's info '''

	baner = Figlet(font='slant')
	print(f'\033[31m{baner.renderText("Pmap")}\033[00m')
	print('\t Made by \033[32mhttps://github.com/Kigrok\033[00m')
	print('\n' + ('-' * 30))
	print(f'Name: \033[36mhttp://{name.strip()}\033[00m')
	print(f'IP: \033[36m{ip}\033[00m')
	print(f'''Country: \033[34m{info(ip = ip)[0]} | {info(ip = ip)[3]}\033[00m\n\
Sity: \033[34m{info(ip = ip)[1]}\033[00m\n\
TimeZone: \033[34m{info(ip = ip)[2]}\033[00m''')
	print(f'Scanning start: \033[36m{str(datetime.now().time().strftime("%H:%M:%S"))}\033[00m')
	print(('-' * 30) + '\n')


def scan_port(port):

	''' Output open port and info '''

	sock = socket.socket()
	sock.settimeout(3)
	try:
		sock.connect((ip, int(port)))
		try:
			print(f'''[\033[31m+\033[00m] \
Port: \033[95m{port}\033[00m \
~ \033[93m{sock.recv(2048).strip().decode("ascii")}\033[00m''')
		except :
			try:
				print(f'''[\033[31m+\033[00m] \
Port: \033[95m{port}\033[00m \
~ \033[93m{sock.recv(1024)}\033[00m''')
			except:
				try:
					print(f'''[\033[31m+\033[00m] \
Port: \033[95m{port}\033[00m \
~ \033[93m{requests.get(f'http://{ip}:{port}', timeout = 5)}\033[00m''')
				except:
					print(f'''[\033[31m+\033[00m] \
Port: \033[95m{port}\033[00m''')

	except: pass
	sock.close()


def processing(options = None, threads = int(multiprocessing.cpu_count())):

	try:
		with multiprocessing.Pool(int(threads)) as process:

			if options == None:

				process.map(scan_port, range(65535))

			else:

				if '-' in options:
					process.map(scan_port, range(int(options.split('-')[0]), (int(options.split('-')[-1])+1)))

				elif '/' in options:
					process.map(scan_port, range(int(options.split('/')[0]), (int(options.split('/')[-1])+1)))

				elif ',' in options:
					process.map(scan_port, options.split(','))

				else:
					process.map(scan_port, range((0), (int(options.split()[0].strip())+1)))

	except KeyboardInterrupt: pass


def main():

	start = datetime.now()
	global ip

	try:
		ip = socket.gethostbyname(get_args().url)
		banner(name = get_args().url, ip = ip)
		processing(
			options = get_args().port, 
			threads = get_args().threads)
		print('\n' + ('-' * 30))
		print(f'Time: \033[36m{datetime.now() - start}\033[00m')

	except Exception as e:
		print(f'\033[31mConnection Error: {e}\033[00m')



if __name__ == '__main__':
	main()