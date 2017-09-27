/********************************************************************************
** Form generated from reading UI file 'rainbowtables.ui'
**
** Created by: Qt User Interface Compiler version 5.5.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_RAINBOWTABLES_H
#define UI_RAINBOWTABLES_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_RainbowTablesClass
{
public:
    QAction *actionExit;
    QAction *actionHelp;
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QVBoxLayout *verticalLayout_2;
    QPushButton *pushButton;
    QLabel *TextLabel;
    QMenuBar *menuBar;
    QMenu *menuFile;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *RainbowTablesClass)
    {
        if (RainbowTablesClass->objectName().isEmpty())
            RainbowTablesClass->setObjectName(QStringLiteral("RainbowTablesClass"));
        RainbowTablesClass->resize(561, 566);
        actionExit = new QAction(RainbowTablesClass);
        actionExit->setObjectName(QStringLiteral("actionExit"));
        actionHelp = new QAction(RainbowTablesClass);
        actionHelp->setObjectName(QStringLiteral("actionHelp"));
        centralWidget = new QWidget(RainbowTablesClass);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        verticalLayout->setSizeConstraint(QLayout::SetNoConstraint);
        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        pushButton = new QPushButton(centralWidget);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(pushButton->sizePolicy().hasHeightForWidth());
        pushButton->setSizePolicy(sizePolicy);

        verticalLayout_2->addWidget(pushButton);

        TextLabel = new QLabel(centralWidget);
        TextLabel->setObjectName(QStringLiteral("TextLabel"));
        TextLabel->setAlignment(Qt::AlignCenter);

        verticalLayout_2->addWidget(TextLabel);

        verticalLayout_2->setStretch(0, 1);

        verticalLayout->addLayout(verticalLayout_2);

        RainbowTablesClass->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(RainbowTablesClass);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 561, 21));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QStringLiteral("menuFile"));
        RainbowTablesClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(RainbowTablesClass);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        RainbowTablesClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(RainbowTablesClass);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        RainbowTablesClass->setStatusBar(statusBar);

        menuBar->addAction(menuFile->menuAction());
        menuFile->addAction(actionExit);

        retranslateUi(RainbowTablesClass);
        QObject::connect(actionExit, SIGNAL(triggered()), RainbowTablesClass, SLOT(close()));
        QObject::connect(pushButton, SIGNAL(clicked()), RainbowTablesClass, SLOT(buttonClick()));

        QMetaObject::connectSlotsByName(RainbowTablesClass);
    } // setupUi

    void retranslateUi(QMainWindow *RainbowTablesClass)
    {
        RainbowTablesClass->setWindowTitle(QApplication::translate("RainbowTablesClass", "RainbowTables", 0));
        actionExit->setText(QApplication::translate("RainbowTablesClass", "Exit", 0));
        actionHelp->setText(QApplication::translate("RainbowTablesClass", "Help", 0));
        pushButton->setText(QApplication::translate("RainbowTablesClass", "Push Me!", 0));
        TextLabel->setText(QString());
        menuFile->setTitle(QApplication::translate("RainbowTablesClass", "File", 0));
    } // retranslateUi

};

namespace Ui {
    class RainbowTablesClass: public Ui_RainbowTablesClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_RAINBOWTABLES_H
