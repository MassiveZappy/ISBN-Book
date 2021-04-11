
## _Get ISBN_:
##### The "simple" "little" isbn api.
You can look in the "Versions" folder to find one :)
You can also see the changelog inside of it.

# Setup:

### Python:
You may need a 3.7+ version of python, get it here!
https://www.python.org/ftp/python/3.9.4/
### PyYAML:
A simple little more human-friendly version of json used in some versions.
- Open a Terminal or Console.
- Run (MacOs):
```sh
pip install pyyaml
```
- Run (Windows):
```sh
pip3 install pyyaml
```
Still don't work?
Do the age old trick, if one of them won't work, just use the other!
I cannot verify the windows command :(

# How to use:
Currently, I am trying to update the app as much as posible.
I will add to this section once I have a final product.
But I will give some pointers.


##### 1.1.0 - 1.2.1

You will find a variable wraped inside of quotes. 
```python
isbn = '34535433'#These numbers are not real, replace the with another isbn
```
Replace that string with anoter and it will retun/create the cover art and other data.
You may only input one ISBN.
##### 1.2.2+
At the top of the main.py file, you will find a variable
```python
Isbns = ['Stuff', 'Another-Stuff', 'More-Stuff']
```
Enter in ISBNS soronded by qotes (doubble or single) and seperated py a comma.
If you only want to use one, just do ["isbn"].
### -"MassiveZappy"
