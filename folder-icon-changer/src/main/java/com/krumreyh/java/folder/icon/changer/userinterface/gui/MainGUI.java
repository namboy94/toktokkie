package com.krumreyh.java.folder.icon.changer.userinterface.gui;

import java.awt.Checkbox;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import com.krumreyh.java.krumreylib.gui.swing.GUITemplate;

/**
 * Class that implements a basic GUI for the program
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainGUI extends GUITemplate{

	private boolean multi = false;
	
	/**
	 * Constructor that adds all elements of the GUI and makes the GUI visible
	 */
	public MainGUI() {
		this.setGUISettings("Folder Icon Changer", 400, 400, 400, 170, null, EXIT_ON_CLOSE, false);
		this.addTextField("", 10, 10, 200, 40);
		this.addButton("Start", 220, 10, 170, 40, null);
		Checkbox multiBox = this.addCheckBox("Multi-Change", 150, 60, 150, 20);
		this.multi = multiBox.getState();
		this.startGUI();
	}
	
	/**
	 * Starts the folder icon changing algorithm
	 */
	protected class StartButton implements ActionListener {

		/**
		 * The performed action on button-press
		 */
		public void actionPerformed(ActionEvent arg0) {
			
		}
	}
}