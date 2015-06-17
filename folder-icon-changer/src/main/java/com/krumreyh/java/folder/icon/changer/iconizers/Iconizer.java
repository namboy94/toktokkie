package com.krumreyh.java.folder.icon.changer.iconizers;

import java.io.File;
import java.io.FileNotFoundException;

import com.krumreyh.java.krumreylib.fileops.FileHandler;

/**
 * Interface that prescribes which methods an iconizer must use to rename icons.
 * @author Hermann Krumrey
 * @version 1.0
 */
public abstract class Iconizer {

	protected File directory;
	protected Mode mode;
	
	/**
	 * Checks what type of iconizing should be performed
	 */
	protected void establishType() {
		File[] children = FileHandler.getDirectoryContent(this.directory);
		for (int i = 0; i < children.length; i++) {
			if (FileHandler.getPureFileName(children[i]).equals("Folder Icon")) {
				this.mode = Mode.SINGLE;
				return;
			}
		}
		this.mode = Mode.MULTI;
	}
	
	//TODO Replace with method from krumreylib (findChild)
	/**
	 * Finds the folder icon directory of a directory
	 * @param directory - the directory to be checked
	 * @return the folder icon directory
	 * @throws FileNotFoundException - in case no Folder Icon Directory was found
	 */
	protected File findFolderIconDirectory(File directory) throws FileNotFoundException {
		File[] children = FileHandler.getDirectoryContent(directory);
		for (int i = 0; i < children.length; i++) {
			if (FileHandler.getPureFileName(children[i]).equals("Folder Icon")) {
				return children[i];
			}
		}
		throw new FileNotFoundException("Folder Icon Folder Not Found");
	}
	
	protected void iconizeSingle() {
		
	}
	
	/**
	 * Starts the iconizing process
	 */
	public abstract void iconize();
	
	protected interface commandType {
		
	}
	
	protected enum Mode {
		SINGLE, MULTI
	}
	
}
