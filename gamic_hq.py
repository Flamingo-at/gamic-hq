import json
import asyncio
import aiohttp

from re import findall
from web3.auto import w3
from loguru import logger
from aiohttp import ClientSession
from random import choice, randint
from aiohttp_proxy import ProxyConnector
from eth_account.messages import encode_defunct
from pyuseragents import random as random_useragent


def random_tor_proxy():
    proxy_auth = str(randint(1, 0x7fffffff)) + ':' + \
        str(randint(1, 0x7fffffff))
    proxies = f'socks5://{proxy_auth}@localhost:' + str(choice(tor_ports))
    return(proxies)


def get_connector():
    connector = ProxyConnector.from_url(random_tor_proxy())
    return(connector)


async def create_email(client: ClientSession):
    try:
        response = await client.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = (await response.json())[0]
        return email
    except:
        logger.error("Failed to create email")
        await asyncio.sleep(1)
        return(await create_email(client))


async def check_email(client: ClientSession, login: str, domain: str, count: int):
    try:
        response = await client.get('https://www.1secmail.com/api/v1/?action=getMessages&'
                                    f'login={login}&domain={domain}')
        email_id = (await response.json())[0]['id']
        return(email_id)
    except:
        while count < 30:
            count += 1
            await asyncio.sleep(1)
            return(await check_email(client, login, domain, count))
        logger.error('Emails not found')
        raise Exception()


async def get_token(client: ClientSession, login: str, domain: str, email_id):
    try:
        response = await client.get('https://www.1secmail.com/api/v1/?action=readMessage&'
                                    f'login={login}&domain={domain}&id={email_id}')
        data = (await response.json())['htmlBody']
        token = findall(
            r'https:\/\/xy1kf6d4.r.us-east-1.awstrack.me\/L0\/https:%2F%2Fgamic.app%2Flogin%3FbindEmailToken=(\S{36})', data)[0]
        return(token)
    except:
        logger.error('Failed to get token')
        raise Exception()


async def wallet_connection(client: ClientSession, address: str, signature: str, session: str):
    response = await client.post('https://gamic.app/api/login/web3',
                                 data={
                                     "address": address,
                                     "signature": signature
                                 }, headers={'cookie': session})
    data = '{' + (str(response.headers)[18:-2]).replace("'", '"') + '}'
    access_token = ((json.loads(data))['Set-Cookie']).split(';')[0]
    check((await response.json())['message'])
    return(access_token)


async def add_ref(client: ClientSession, email: str):
    try:
        response = await client.post('https://gamic.app/api/user/create',
                                     json={
                                         "avatar": "https://storage.googleapis.com/gamic-prod/user/avator/portrait.svg",
                                         "username": email.split("@")[0],
                                         "role": "ROLE_GAME_USER",
                                         "inviterId": ref
                                     })
        return(await response.json())['result']['id']
    except:
        raise Exception()


def check(message: str):
    if 'Success' != message:
        logger.error(message)
        raise Exception()


def create_wallet():
    account = w3.eth.account.create()
    return(str(account.address), str(account.privateKey.hex()))


def create_signature(private_key: str, nonce: str):
    message = encode_defunct(text=nonce)
    signed_message = w3.eth.account.sign_message(message, private_key)
    return(signed_message.signature.hex())


async def worker():
    while True:
        try:
            async with aiohttp.ClientSession(
                connector=get_connector(),
                headers={'user-agent': random_useragent()}
            ) as client:

                logger.info('Get nonce')
                response = await client.get('https://gamic.app/api/login/web3/message')
                nonce = (await response.json())['result']

                data = str(response.headers)
                index = data.index('SESSION=')
                session = data[index:index + 56]

                address, private_key = create_wallet()
                signature = create_signature(private_key, nonce)

                logger.info('Wallet connection')
                access_token = await wallet_connection(client, address, signature, session)

                logger.info('Create email')
                email = await create_email(client)

                client.headers.update({'cookie': f'{id};{access_token}'})

                logger.info('Add referral code')
                referrer_code = await add_ref(client, email)
                
                logger.info('Joining the GamicHQ community')
                response = await client.post('https://gamic.app/api/guild/join/community/20', data={})
                check((await response.json())['message'])

                logger.info('Joining the Gamic Gaming community')
                response = await client.post('https://gamic.app/api/guild/join/community/10', data={})
                check((await response.json())['message'])

                logger.info('Bind email')
                response = await client.post('https://gamic.app/api/user/bindEmailSend',
                                             data={'email': email})
                check((await response.json())['message'])

                logger.info('Check email')
                email_id = await check_email(client, email.split('@')[0], email.split('@')[1], 0)

                token = await get_token(client, email.split('@')[0], email.split('@')[1], email_id)

                logger.info('Email confirmation')
                await client.post(f'https://gamic.app/api/user/bindEmail?token={token}')

                response = await client.post('https://gamic.app/api/point/register', data={})
                check((await response.json())['message'])

        except Exception:
            logger.error("Error\n")
        else:
            with open('registered.txt', 'a', encoding='utf-8') as file:
                file.write(f'{email}:{address}:{private_key}\n')
            logger.success('Successfully\n')

        await asyncio.sleep(delay)


async def main():
    tasks = [asyncio.create_task(worker()) for _ in range(threads)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    tor_ports = [9150]

    print("Bot Gamic.app @flamingoat\n")

    ref = input('Referral code: ')
    delay = int(input('Delay(sec): '))
    threads = int(input('Threads: '))

    asyncio.run(main())
