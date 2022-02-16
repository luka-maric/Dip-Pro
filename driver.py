import os
import RPi.GPIO as GPIO
import time
import numpy

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
'''Postavljanje GPIO logike
'''


class DM542:

	def __init__(self, step_pin, dir_pin, ena_pin):
		self.step_pin = step_pin
		self.dir_pin = dir_pin
		self.ena_pin = ena_pin
		'''Zadavanje pina/pinova (lako dodamo) na kojeg spajamo
		'''

	def pokretanje_steppera(self):
		'''
		Jednostavno testiranje ispravnosti drivera
		'''

		GPIO.setup(self.step_pin, GPIO.OUT)
		GPIO.setup(self.dir_pin, GPIO.OUT)
		GPIO.setup(self.ena_pin, GPIO.OUT)
		'''Definiranje zadanih pinova kao outpute kojima dodijeljujemo naponske razine
		'''

		try: 
			i = 0
			while i in range(1000000):
				i += 1
				time.sleep(0.001)
				GPIO.output(self.step_pin, GPIO.HIGH)
				time.sleep(0.001)
				GPIO.output(self.step_pin, GPIO.LOW)
				'''Pomicanje stepper motora
				'''
		except KeyboardInterrupt:
			GPIO.cleanup()
			print("Kraj!")

		GPIO.output(self.dir_pin, GPIO.HIGH)
		GPIO.output(self.ena_pin, GPIO.HIGH)

#Primjer pozivanja

#radi = DM542(26,19,13)
#radi.pokretanje_steppera()
 

	def koraci(broj_koraka, frekvencija):
		'''
		broj_koraka -> Broj koraka potreban da stepper motor napravi rotaciju od 360' -> datasheet?
		frekvencija -> Solidna praksa (bez mikrostepa) je 1/n (sekunda/broj koraka)
		'''
		brojac = 0
		while brojac < broj_koraka:
			brojac += 1
			time.sleep(frekvencija)
			GPIO.output(self.step_pin, GPIO.HIGH)
			time.sleep(frekvencija)
			GPIO.output(self.step_pin, GPIO.LOW)



	def devedeset(smjer,period):
		'''
		Smjer -> 1 = smjer kazaljke na satu | 0 = smjer kontra kazaljke na satu (True/False su alternativni inputi)
		Period -> Ovisno o vremenskim intervalima u kojima se za normalan način rada kamera treba pomicati na sljedeći uređaj
		'''

		try:
			while True:
				GPIO.setup(self.step_pin, GPIO.OUT)
				GPIO.setup(self.dir_pin, GPIO.OUT)
				GPIO.setup(self.ena_pin, GPIO.OUT)
				GPIO.output(self.dir_pin, smjer)
				for i in range(4):
					DM542.koraci(200/4, 0.005)
					#uzeto za primjer da je potrebno 200 koraka
					time.sleep(period)
		except KeyboardInterrupt:
			GPIO.cleanup()
			print("Kraj!")

#Primjer pozivanja

#radi = DM542(26,19,13)
#DM542.devedeset(1, 10)

	def ciljani_kut(smjer, kut, frekvencija, korak):
		GPIO.output(dir_pin, smjer)
		koraci_do_kuta = (float(kut) / float(360)) * korak 
		'''
		Kalkulira točan broj koraka da se pomakne na određeni kut -> bitno je imati referencu za 0
		'''
		pauza = 1 / ((float(frekvencija) * korak) / 60)
		while koraci_do_kuta > 0:
			GPIO.output(step_pin, HIGH)
			time.sleep(pauza / 2)
			GPIO.output(step_pin, LOW)
			time.sleep(pauza / 2)
			koraci_do_kuta -= 1

