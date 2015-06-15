package com.krumreyh.java.folder.icon.changer.iconizers;

/**
 * Interface that prescribes which methods an iconizer must use to rename icons.
 * @author Hermann Krumrey
 * @version 1.0
 */
public interface Iconizer {
	
	/**
	 * Changes A single show's worth of folder icons
	 */
	public void changeIconsSingleFolder();
	
	/**
	 * Changes Multiple Show's worth of Folder Icons
	 */
	public void changeIconsMultiFolder();
	
}
