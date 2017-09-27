#include "rainbowtables.h"

RainbowTables::RainbowTables(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	clickCounter = 0;
}

RainbowTables::~RainbowTables() {}

void RainbowTables::buttonClick() {
	clickCounter++;
	QString message = "Clicks: ";
	message.append(QString::number(clickCounter));
	ui.TextLabel->setText(message);
}
