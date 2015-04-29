# genderator

Genderator is a Python library to process spanish names to guess their gender.

For this to work, the libray uses the next datasets from [Instituto Nacional de Estadística](http://www.ine.es):

- **name_surname_ratio**: List of words that could be both, a name or a surname, and shows the probability to be a surname.
- **names_ine**: List of registered names on Spain, with the probability for each one to be a male or a female name.
- **surnames_ine**: List of registeres surnames on Spain.

## Installation

The easiest way to install the latest version is by using pip to pull it from PyPI:
```
pip install genderator
```
You may also use Git to clone the repository from Github and install it manually:
```
git clone https://github.com/davidmogar/genderator.git
cd genderator
python setup.py install
```

## Usage

The next code shows a sample usage of this library:

```python
import collections
import genderator
import json

guesser = genderator.Parser()
answer = guesser.guess_gender('David Moreno García')
if answer:
    # Keep returned keys order
    parsed = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(answer)
    print(json.dumps(parsed, indent=4))
else:
    print('No answer')
```
Output:
```json
{
    "names": {
        "david": 0.991
    },
    "surnames": {
        "moreno": 1.0
    },
    "real_name": "david",
    "gender": "Male",
    "confidence": 1.0
}
```
