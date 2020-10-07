import os

from ctm import Client

ACCOUNT = os.environ.get('CTM_ACCOUNT_ID')
TOKEN   = os.environ.get('CTM_TOKEN')
SECRET  = os.environ.get('CTM_SECRET')


client = Client(ACCOUNT, TOKEN, SECRET, 30, os.environ.get('CTM_HOST'))

after = None

while True:

  # loop over calls, page size can be up to 1000 when limiting to fewer than 12 fields otherwise page size is limited to 100
  ret, data = client.calls({'after': after, 'limit_fields': ['id','name'], 'per_page': 1000})

  # if we get anything other than a 200 something went wrong and we should either exponentially back off or try again later
  if ret != 200:
    break

  calls = data['calls']

  # if there is nothing in the last page requested stop
  if len(calls) == 0:
    break

  print(calls)

  # access the next page token e.g. request everything after the given token
  after = data.get('after', None)

  if after == None:
    break
