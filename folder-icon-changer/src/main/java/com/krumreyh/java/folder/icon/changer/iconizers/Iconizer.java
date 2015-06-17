package com.krumreyh.java.folder.icon.changer.iconizers;

import java.io.File;
import java.io.FileNotFoundException;

import com.krumreyh.java.folder.icon.changer.objects.Icon;
import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Class that handles the iconizing of folders
 * @author Hermann Krumrey
 * @version 1.0
 */
public class Iconizer {

	protected File[] children;
	
	/**
	 * Constructor that checks if the give directory is valid and saves its children to a File array
	 * @param directory
	 * @throws IllegalArgumentException - in case the directory is invalid
	 */
	public Iconizer(String directory) throws IllegalArgumentException {
		if (!FileHandler.checkIfDirectory(directory)) { throw new IllegalArgumentException("Not a valid directory"); }
		this.children = FileHandler.getDirectoryContent(new File(directory));
	}
	
	protected void iconize(IconCommand iconcom) {
		for (int i = 0; i < this.children.length; i++) {
			File folderIconFolder = null;
			File[] innerChildren = FileHandler.getDirectoryContent(this.children[i]);
			for (int j = 0; j < innerChildren.length; j++) {
				if (innerChildren[i].getName().equals("Folder Icon")) {
					folderIconFolder = innerChildren[j];
					break;
				}
			}
			iconcom.iconize(this.children[i], folderIconFolder, "Main");
			iconcom.iconize(folderIconFolder, folderIconFolder, "Folder Icon");
			for (int j = 0; j < innerChildren.length; j++) {
				if (innerChildren[j].getName().equals("Folder Icon")) {
					continue;
				}
				if (FileHandler.checkIfDirectory(innerChildren[j])) {
					iconcom.iconize(innerChildren[j], folderIconFolder);
					if (FileHandler.hasChildren(innerChildren[j])) {
						recursiveIconize(innerChildren[j], iconcom, folderIconFolder);
					}
				}
			}
		}
	}
	
	protected void recursiveIconize(File directory, IconCommand iconcom, File folderIconFolder) {
		File[] children = FileHandler.getDirectoryContent(directory);
		for (int i = 0; i < children.length; i++) {
			if (FileHandler.checkIfDirectory(children[i])) {
				iconcom.iconize(children[i], folderIconFolder);
				if (FileHandler.hasChildren(children[i])) {
					recursiveIconize(children[i], iconcom, folderIconFolder);
				}
			}
		}
	}
	
	protected interface IconCommand {
		public void iconize(File folder, File icon);
		
		public void iconize(File folder, File icon, String hardcoded);
	}
	
}
