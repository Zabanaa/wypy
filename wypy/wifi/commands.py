from .wifi import WiFi
import click


@click.group('wifi')
def wifi():
    pass


@click.command('on')
def turn_wifi_on():
    wifi = WiFi()
    wifi.turn_on()


@click.command('off')
def turn_wifi_off():
    wifi = WiFi()
    wifi.turn_off()


@click.command('status')
def wifi_status():
    wifi = WiFi()
    wifi.print_status()


wifi.add_command(turn_wifi_on)
wifi.add_command(turn_wifi_off)
wifi.add_command(wifi_status)
