<h1 align="center">Gamic HQ</h1>

<p align="center">Registration of referrals for the <a href="https://gamic.app/">Gamic.app</a></p>
<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/Tor-7D4698?style=for-the-badge&logo=Tor-Browser&logoColor=white">
</p>

## ⚡ Installation
+ Install [python](https://www.google.com/search?client=opera&q=how+install+python)
+ Install [Tor Browser](https://www.torproject.org/download/)
+ [Download](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github) and unzip repository
+ Install requirements:
```python
pip install -r requirements.txt
```

## 💻 Preparing
+ Launch Tor Browser
+ Run the bot:
```python
python gamic_hq.py
```

## ✔️ Usage
+ ```Referral code``` - your referrals code
  + Example: ```https://gamic.app/s/GamicHQ/u/123456```, code = ```123456```
+ ```Delay(sec)``` - delay between referral registrations in seconds
+ ```Threads``` - number of simultaneous registrations

Temporary email addresses are used to register referrals

**Successfully registered referrals are saved in** ```registered.txt``` **in the format** ```{email}:{address}:{private_key}```

## 📧 Contacts
+ Telegram - [@flamingoat](https://t.me/flamingoat)