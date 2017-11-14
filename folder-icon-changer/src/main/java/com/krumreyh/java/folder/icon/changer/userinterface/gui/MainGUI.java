/*
Copyright 2015-2017 Hermann Krumrey

This file is part of folder-icon-changer.

folder-icon-changer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

folder-icon-changer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with folder-icon-changer.  If not, see <http://www.gnu.org/licenses/>.
*/

package com.krumreyh.java.folder.icon.changer.userinterface.gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JTextField;

import com.krumreyh.java.folder.icon.changer.iconizers.NautilusIconizer;
import com.krumreyh.java.krumreylib.gui.swing.GUITemplate;

/**
 * Class that implements a basic GUI for the program
 * @author Hermann Krumrey
 * @version 1.0
 */
public class MainGUI extends GUITemplate {

	protected JTextField directory;
	protected JComboBox<String> selectedBrowser;
	
	/**
	 * Constructor that adds all elements of the GUI and makes the GUI visible
	 */
	public MainGUI() {
		
		String[] validIconizers = null;
		switch (System.getProperty("os.name")) {
		case "Linux":	validIconizers = new String[] {"Nautilus", "Nemo"};
						break;
		case "Windows":	validIconizers = new String[] {"Explorer"};
						break;
		case "Mac":		validIconizers = new String[] {"Finder"};
						break;
		default:		showPopUpMessage("Unsupported OS detected");
		}
		
		this.setGUISettings("Folder Icon Changer", 400, 400, 400, 110, null, EXIT_ON_CLOSE, false);
		this.directory = this.addTextField("", 10, 10, 200, 40);
		this.addButton("Start", 220, 10, 170, 40, new StartButton());
		this.selectedBrowser = this.addDropDownMenu(validIconizers, 170, 70, 200, 20);
		this.addLabel("OS: " + System.getProperty("os.name"), 80, 60, 100, 40);
		
		this.startGUI();
	}
	
	/**
	 * Starts the folder icon changing algorithm
	 */
	protected class StartButton implements ActionListener {

		/**
		 * The performed action on button-press
		 * @param e - the button-press event
		 */
		public void actionPerformed(ActionEvent e) {
			try {
				switch (System.getProperty("os.name")) {
				case "Linux":		switch((String) MainGUI.this.selectedBrowser.getSelectedItem()) {
				case "Nemo":		
				case "Nautilus":	new NautilusIconizer(MainGUI.this.directory.getText()).iconize();
									break;
				default:			}
									break;
				case "Windows":		switch((String) MainGUI.this.selectedBrowser.getSelectedItem()) {
				case "Explorer":	break;
				default:			}
									break;
				case "Mac":			switch((String) MainGUI.this.selectedBrowser.getSelectedItem()) {
				case "Finder":		break;
				default:			}
									break;
				default:			showPopUpMessage("Unsupported OS detected");
				}
				showPopUpMessage("Operation completed");
				
			} catch (IllegalArgumentException ex) {
				showPopUpMessage(ex.getMessage());
			}	
		}
	}
}