### INSTALLATION:
1. git clone https://github.com/DenMaslov/dz5.git
2. cd dz5
3. cd files_utility


### for usage:
  1. py main.py --operation move --src D:\\b...\\ --to D:\\a...\\ --threads 10
  2. py main.py --operation copy --src D:\\b...\\c*.py --to D:\\a...\ --threads 5
  3. py main.py --operation copy --src D:\\b...\\test*.git --to D:\\a...\ 
  4. etc

### Each copying/ moving call runs in thread pool

### TESTED WITH:
* Windows 10
* python 3.9
