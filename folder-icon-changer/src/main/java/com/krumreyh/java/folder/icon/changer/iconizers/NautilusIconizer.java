package com.krumreyh.java.folder.icon.changer.iconizers;

import java.io.File;

import com.krumreyh.java.krumreylib.fileops.FileHandler;

public class NautilusIconizer implements Iconizer{

	private File upperDirectory;
	private File[] folderIcons;
	
	/**
	 * Constructor that checks if the given directory exists and is valid
	 * @param directory - the directory containing the folders to be iconized
	 * @throws IllegalArgumentException - In case the directory is invalid
	 */
	public NautilusIconizer(String directory) throws IllegalArgumentException {
		if (!FileHandler.checkIfDirectory(directory)) {
			throw new IllegalArgumentException("Not a valid directory");
		} else {
			this.upperDirectory = new File(directory);
		}
	}
	
	public void searchForFolderIcons(File[] parentChildren) {
		for (int i = 0; i < parentChildren.length; i++) {
			if (FileHandler.getPureFileName(parentChildren[i]).equals("Folder Icon")) { 
				this.folderIcons = FileHandler.getDirectoryContent(parentChildren[i]);
				return;
			}
		}
		throw new IllegalStateException("No Folder Icon Folder Found");
	}
	
	public void changeIconsSingleFolder() {
		File[] firstChildren = FileHandler.getDirectoryContent(this.upperDirectory);
		searchForFolderIcons(firstChildren);
		
	}

	public void changeIconsMultiFolder() {
		// TODO Auto-generated method stub
		
	}
}
