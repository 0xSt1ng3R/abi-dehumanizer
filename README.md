# Human-Readable ABI String Convertor To eth_abi Compatible List

This repository contains Python classes designed for parsing human-readable ABI strings into a format that can be easily used with the `eth_abi.decode()` function.


## Installation

```
pip install abi_dehumanizer
```


## Usage

```python
>>> from abi_dehumanizer import ABIDehumanizer
>>> ABIDehumanizer("deposit((address,uint256,uint256,uint256,(address,address,bool,uint256)[]),address[],uint256[])").parse_parameters()
['(address,uint256,uint256,uint256,(address,address,bool,uint256)[])', 'address[]', 'uint256[]']
>>> 
>>> ABIDehumanizer("claim(address,address,uint256,uint256,bytes32[])").parse_parameters()
['address', 'address', 'uint256', 'uint256', 'bytes32[]']
>>> 
>>> ABIDehumanizer("transfer(address,uint256)").parse_parameters()
['address', 'uint256']
```