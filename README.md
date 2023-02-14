# wallet-desktop

templated repository for building non-custodial desktop wallet in python on top of the xrp ledger, by utilizing the xrpl library.  the application will allow for users to see updates on the xrp ledger, view ledger activities, see accounts reserve requirements, send direct xrp payments and provide feedback about the intended destination address.  in addition to learning the implementation of these features, this repository will also contain a graphical user interface, threading, and asynchronous `async` code in python.

**contents**

1.  [requirements](#requirements)
2.  [application capabilities](#application-capabilities)
3.  [readme](https://github.com/XRPLF/xrpl-dev-portal/blob/master/content/tutorials/build-apps/build-a-desktop-wallet-in-python.md)
4.  [learning portal](https://xrpl.org/build-a-desktop-wallet-in-python.html)
5.  [dependencies](#dependencies)
-   [notes](#notes)

![Uploading Screenshot 2023-02-13 at 9.51.53 PM.png…]()


## requirements

1.  `xrpl-py==1.3.0`
2.  `wxPython==4.1.1`
3.  `toml==0.10.2`
4.  `requests==2.25.1`

## application capabilities

1.  shows updates to the xrp ledger in real-time
2.  can view any xrp ledger account's activities "read-only" including showing how much xrp was delivered by each transaction
3.  shows how much xrp is set aside for the account's reserve requirement
4.  can send direct xrp payments and provide feedback about the intended destination address, the feedback includes
    - whether the intended destination already exists in the xrp ledger, or the payment would have to fund its creation
    - if the address does not wan to recieve xrp `DisallowXRP` is set to `true` / it's flag is emabled
    - if the address has a verified domain name associated with it

## dependencies

1.  `xrpl-py` a client library for the xrp ledger
2.  `wxPython` a cross platform graphical toolkit
3.  `requests` a library for making http requests

```zsh
❯ pip3 install --upgrade xrpl-py wxPython requests toml
Requirement already satisfied: xrpl-py in /opt/homebrew/lib/python3.10/site-packages (1.3.0)
Collecting xrpl-py
  Downloading xrpl_py-1.7.0-py3-none-any.whl (208 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 208.0/208.0 kB 932.0 kB/s eta 0:00:00
Requirement already satisfied: wxPython in /opt/homebrew/lib/python3.10/site-packages (4.2.0)
Collecting requests
  Using cached requests-2.28.2-py3-none-any.whl (62 kB)
Collecting toml
  Using cached toml-0.10.2-py2.py3-none-any.whl (16 kB)
Requirement already satisfied: websockets<11.0,>=10.0 in /opt/homebrew/lib/python3.10/site-packages (from xrpl-py) (10.4)
Collecting types-Deprecated<2.0.0,>=1.2.9
  Downloading types_Deprecated-1.2.9-py3-none-any.whl (3.2 kB)
Collecting typing-extensions<5.0.0,>=4.2.0
  Downloading typing_extensions-4.4.0-py3-none-any.whl (26 kB)
Requirement already satisfied: base58<3.0.0,>=2.1.0 in /opt/homebrew/lib/python3.10/site-packages (from xrpl-py) (2.1.1)
Requirement already satisfied: ECPy<2.0.0,>=1.2.5 in /opt/homebrew/lib/python3.10/site-packages (from xrpl-py) (1.2.5)
Requirement already satisfied: httpx<0.19.0,>=0.18.1 in /opt/homebrew/lib/python3.10/site-packages (from xrpl-py) (0.18.2)
Collecting Deprecated<2.0.0,>=1.2.13
  Downloading Deprecated-1.2.13-py2.py3-none-any.whl (9.6 kB)
Requirement already satisfied: numpy in /opt/homebrew/lib/python3.10/site-packages (from wxPython) (1.23.5)
Requirement already satisfied: pillow in /opt/homebrew/lib/python3.10/site-packages (from wxPython) (9.3.0)
Requirement already satisfied: six in /opt/homebrew/lib/python3.10/site-packages (from wxPython) (1.16.0)
Collecting urllib3<1.27,>=1.21.1
  Using cached urllib3-1.26.14-py2.py3-none-any.whl (140 kB)
Requirement already satisfied: idna<4,>=2.5 in /opt/homebrew/lib/python3.10/site-packages (from requests) (3.4)
Collecting charset-normalizer<4,>=2
  Using cached charset_normalizer-3.0.1-cp310-cp310-macosx_11_0_arm64.whl (122 kB)
Requirement already satisfied: certifi>=2017.4.17 in /opt/homebrew/lib/python3.10/site-packages (from requests) (2022.12.7)
Collecting wrapt<2,>=1.10
  Downloading wrapt-1.14.1-cp310-cp310-macosx_11_0_arm64.whl (35 kB)
Requirement already satisfied: rfc3986[idna2008]<2,>=1.3 in /opt/homebrew/lib/python3.10/site-packages (from httpx<0.19.0,>=0.18.1->xrpl-py) (1.5.0)
Requirement already satisfied: sniffio in /opt/homebrew/lib/python3.10/site-packages (from httpx<0.19.0,>=0.18.1->xrpl-py) (1.3.0)
Requirement already satisfied: httpcore<0.14.0,>=0.13.3 in /opt/homebrew/lib/python3.10/site-packages (from httpx<0.19.0,>=0.18.1->xrpl-py) (0.13.7)
Requirement already satisfied: h11<0.13,>=0.11 in /opt/homebrew/lib/python3.10/site-packages (from httpcore<0.14.0,>=0.13.3->httpx<0.19.0,>=0.18.1->xrpl-py) (0.12.0)
Requirement already satisfied: anyio==3.* in /opt/homebrew/lib/python3.10/site-packages (from httpcore<0.14.0,>=0.13.3->httpx<0.19.0,>=0.18.1->xrpl-py) (3.6.2)
Installing collected packages: types-Deprecated, charset-normalizer, wrapt, urllib3, typing-extensions, toml, requests, Deprecated, xrpl-py
  Attempting uninstall: typing-extensions
    Found existing installation: typing-extensions 3.10.0.2
    Uninstalling typing-extensions-3.10.0.2:
      Successfully uninstalled typing-extensions-3.10.0.2
  Attempting uninstall: xrpl-py
    Found existing installation: xrpl-py 1.3.0
    Uninstalling xrpl-py-1.3.0:
      Successfully uninstalled xrpl-py-1.3.0
Successfully installed Deprecated-1.2.13 charset-normalizer-3.0.1 requests-2.28.2 toml-0.10.2 types-Deprecated-1.2.9 typing-extensions-4.4.0 urllib3-1.26.14 wrapt-1.14.1 xrpl-py-1.7.0

~                                                                                         5s 09:33:27 PM
❯
```

## notes

1.  reserves

the xrp ledger applies _reserve requirements_, in xrp, to protect the shared global ledger from growing excessively large as the result malicious usage.  the goal is to constrain the growth of the ledger to match improvements in technology so that a current commodity-level machine can always fit the current ledger in RAM.  in order to have an account, an address must hold a minimum amount of xrp in the shared global ledger.  to fund a new address, you must receive enough xrp at that address to meet the reserve requirement.  you cannot send the reserved xrp to others, but you can recover some of the xrp by deleting the account.  the reserve requirements change due to the fee voting process, where [validators](https://livenet.xrpl.org/network/validators)

**university of kansas validator / domain ripple.ittc.ku.edu**

- master key:  `nHUVPzAmAmQ2QSc4oE1iLfsGi17qN2ado8PhxvgEkou76FLxAz7C`
- version:  `1.9.4`
- signing key:  `n9J1GJHtua77TBEzir3FvsgWX68xBFeC8os3s5TkCg97E1cwxKfH`
- ledger:  `31E44F125EFFD7AA146407F9020A5D509E70C19DD05B7492D14ECAD9EE3EFED7`
- unl: [vl.ripple.com](vl.ripple.com)

2.  base reserve and owner reserve

reserve requirements
