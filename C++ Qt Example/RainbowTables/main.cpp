#include "rainbowtables.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	RainbowTables w;
	w.show();
	return a.exec();
}
