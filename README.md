# PCMS

PCMS is intended to be a In-Car-Infotainment System which can be run off a Raspberry Pi, expanding older Cars for Bluetooth and Infotainment functionalities.

## Getting Started

Just clone this repo, run main.py, and connect your mobile phone via Bluetooth.
Make sure bluez and ofono daemon are running, else it won't work.

### Prerequisites

To run this project, you need at last

```
bluez
ofono
pydbus
kivy
vobject
python-gobject
python-can
```

## Built With

* [Kivy](http://kivy.org) - Graphics Framework
* [VObject] (http://eventable.github.io/vobject/) - For parsing VCards
* [python-can] (https://github.com/hardbyte/python-can) - CAN support

## Authors

* **Maximilian Zander** - *Initial work* - [zandemax](https://github.com/zandemax)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details
