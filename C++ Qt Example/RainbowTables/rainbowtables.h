#ifndef RAINBOWTABLES_H
#define RAINBOWTABLES_H

#include <QtWidgets/QMainWindow>
#include "ui_rainbowtables.h"

class RainbowTables : public QMainWindow
{
	Q_OBJECT

public:
	RainbowTables(QWidget *parent = 0);
	~RainbowTables();

public slots:
	void buttonClick();

private:
	Ui::RainbowTablesClass ui;
	unsigned int clickCounter;
};

#endif // RAINBOWTABLES_H
