# haushaltconv
Konvertiert die Haushals-Rohdaten der Stadt Wuppertal in das Format von offenerhaushalt.de // openspending.org

## Quick start

Download https://www.offenedaten-wuppertal.de/dataset/haushaltsplan-entwurf-20182019

```
git clone https://github.com/Opendatal/haushaltconv
git checkout 2018-2019

cd haushaltconv

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python convert.py
```
