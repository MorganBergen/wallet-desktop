# wallet-desktop

templated repository for building non-custodial desktop wallet in python on top of the xrp ledger, by utilizing the xrpl library.

**contents**

1.  [requirements](#requirements)
2.  [application capabilities](#application-capabilities)
3.  [readme](https://github.com/XRPLF/xrpl-dev-portal/blob/master/content/tutorials/build-apps/build-a-desktop-wallet-in-python.md)
4.  [learning portal](https://xrpl.org/build-a-desktop-wallet-in-python.html)
-   [notes](#notes)


## requirements

1.  `xrpl-py==1.3.0`
2.  `wxPython==4.1.1`
3.  `toml==0.10.2`
4.  `requests==2.25.1`

## application capabilities

1.  shows updates to the xrp ledger in real-time
2.  can view any xrp ledger account's activitt "read-only" including showing how much xrp was delivered by each transaction
3.  shows how much xrp is set aside for the account's reserve requirement





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
