# wallet-desktop

templated repository for building non-custodial desktop wallet in python on top of the xrp ledger, by utilizing the xrpl library.  the application will allow for users to see updates on the xrp ledger, view ledger activities, see accounts reserve requirements, send direct xrp payments and provide feedback about the intended destination address.  in addition to learning the implementation of these features, this repository will also contain a graphical user interface, threading, and asynchronous `async` code in python.  the end product will be a non-custodial wallet application that can check an account's balances, send XRP, and nitify when the account receives infomcing transactions.

[mac os building ontop of ripplenet instructions](https://github.com/XRPLF/rippled/blob/5834fbbc5d5f7354f2ba4e8426391f8ff112c744/Builds/macos/README.md)  in this case i will be utilizing homebrew as my package manager therefore no library configuration path necessary

**contents**

0.  [app projects](#app-projects)
1.  [requirements](#requirements)
2.  [application capabilities](#application-capabilities)
3.  [readme](https://github.com/XRPLF/xrpl-dev-portal/blob/master/content/tutorials/build-apps/build-a-desktop-wallet-in-python.md)
4.  [learning portal](https://xrpl.org/build-a-desktop-wallet-in-python.html)
5.  [dependencies](#dependencies)
6.  [notes](#notes)

## app projects

1.  [latest validated ledger index app](https://github.com/MorganBergen/wallet-desktop/tree/main/src/00-get-ledger)
2.  [show ledger updates]()
2.  show ledger updates - `02-threaded.py`

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

## notes

1.  reserves

the xrp ledger applies _reserve requirements_, in xrp, to protect the shared global ledger from growing excessively large as the result malicious usage.  the goal is to constrain the growth of the ledger to match improvements in technology so that a current commodity-level machine can always fit the current ledger in RAM.  in order to have an account, an address must hold a minimum amount of xrp in the shared global ledger.  to fund a new address, you must receive enough xrp at that address to meet the reserve requirement.  you cannot send the reserved xrp to others, but you can recover some of the xrp by deleting the account.  the reserve requirements change due to the fee voting process, where [validators](https://livenet.xrpl.org/network/validators)

**university of kansas validator / domain ripple.ittc.ku.edu**

- master key:  `nHUVPzAmAmQ2QSc4oE1iLfsGi17qN2ado8PhxvgEkou76FLxAz7C`
- version:  `1.9.4`
- signing key:  `n9J1GJHtua77TBEzir3FvsgWX68xBFeC8os3s5TkCg97E1cwxKfH`
- ledger:  `31E44F125EFFD7AA146407F9020A5D509E70C19DD05B7492D14ECAD9EE3EFED7`
- unl: [vl.ripple.com](vl.ripple.com)
