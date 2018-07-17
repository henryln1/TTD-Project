from celery import Celery 
from celery.schedules import crontab
from tests import *

'''
Attempting to learn how to use celery by making our tests.py run every so often.

'''

def periodic_test_run():
	app = Celery()


	@app.on_after_configure.connect


	def setup_periodic_tasks(sender, **kwargs):
		# Calls test('hello') every 10 seconds.
		sender.add_periodic_task(10.0, test.s(), name='add every 10')

	   





	@app.task
	def test():
		run_all_tests()
