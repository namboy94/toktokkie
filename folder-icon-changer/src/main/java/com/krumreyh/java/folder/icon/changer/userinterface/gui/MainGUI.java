package com.krumreyh.java.folder.icon.changer.userinterface.gui;

import java.awt.Checkbox;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JTextField;

import com.krumreyh.java.folder.icon.changer.iconizers.Iconizer;
import com.krumreyh.java.folder.icon.changer.iconizers.NautilusIconizer;
import com.krumreyh.java.krumreylib.gui.swing.GUITemplate;

/**
 * Class that implements a basic GUI for the program
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainGUI extends GUITemplate{

	private JTextField directory;
	
	/**
	 * Constructor that adds all elements of the GUI and makes the GUI visible
	 */
	public MainGUI() {
		this.setGUISettings("Folder Icon Changer", 400, 400, 400, 170, null, EXIT_ON_CLOSE, false);
		this.directory = this.addTextField("", 10, 10, 200, 40);
		this.addButton("Start", 220, 10, 170, 40, new StartButton());
		this.addLabel("OS", 220, 210, 170, 40);
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
			NautilusIconizer iconizer = new NautilusIconizer(MainGUI.this.directory.getText());
			iconizer.iconize();
		}
	}
}