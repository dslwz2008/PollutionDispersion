using UnityEngine;
using System;
using System.Collections;
using System.Data;
//using Mono.Data.Sqlite;
using Mono.Data.SqliteClient;

//C# class for accessing SQLite objects.
public class SqliteDB {
	// variables for basic query access
	private string connection;
	private IDbConnection dbcon;
	private IDbCommand dbcmd;
	private IDataReader reader;

	public void OpenDB(string path){
		connection = "URI=file:" + path; // we set the connection to our database
		dbcon = (IDbConnection)new SqliteConnection(connection);
		dbcon.Open();
	}

	public ArrayList GetTableNames(){
		string query = "select name from sqlite_master where type='table' order by name";
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
		ArrayList readArray = new ArrayList();
		while(reader.Read()){
			readArray.Add(reader.GetValue(0)); 
		}
		return readArray;
	}
	
	public ArrayList ReadLimitLines(string tableName, int startLine, int lineNumbers){
		string query = "SELECT * FROM " + tableName + " LIMIT " + startLine + "," + lineNumbers;
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
		ArrayList readArray = new ArrayList();
		while(reader.Read()){
			var lineArray = new ArrayList();
			for (int i = 0; i < reader.FieldCount; i++){
				lineArray.Add(reader.GetValue(i)); // This reads the entries in a row
			}
			readArray.Add(lineArray); // This makes an array of all the rows
		}
		return readArray; // return matches
	}
		
	public void UpdateSpecificValue(string tableName, string valueColName, string value,
	string clauseColName, string clauseColValue ){
		string query;
		query = "UPDATE " + tableName + " SET " + valueColName + " = " + value +
			" WHERE " + clauseColName + " = \"" + clauseColValue + "\"";
			Debug.Log(query);
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
	}

	public IDataReader BasicQuery(string q, bool r){ // run a baic Sqlite query
		dbcmd = dbcon.CreateCommand(); // create empty command
		dbcmd.CommandText = q; // fill the command
		reader = dbcmd.ExecuteReader(); // execute command which returns a reader
		if(r){ // if we want to return the reader
			return reader; // return the reader
		}else{
			return null;
		}
	}

	public ArrayList ReadFullTable(string tableName){
		string query;
		query = "SELECT * FROM " + tableName;
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
		ArrayList readArray = new ArrayList();
		while(reader.Read()){
			ArrayList lineArray = new ArrayList();
			for (int i = 0; i < reader.FieldCount; i++){
				lineArray.Add(reader.GetValue(i)); // This reads the entries in a row
			}
			readArray.Add(lineArray); // This makes an array of all the rows
		}
		return readArray; // return matches
	}

	// This function deletes all the data in the given table.  Forever.  WATCH OUT! Use sparingly, if at all
	public void DeleteTableContents(string tableName){
		string query;
		query = "DELETE FROM " + tableName;
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
	}

	public void CreateTable(string name, ArrayList col, ArrayList colType){ // Create a table, name, column array, column type array
		string query = "CREATE TABLE " + name + "(" + col[0] + " " + colType[0];
		for(int i = 1; i < col.Count; i++){
			query += ", " + col[i] + " " + colType[i];
		}
		query += ")";
		dbcmd = dbcon.CreateCommand(); // create empty command
		dbcmd.CommandText = query; // fill the command
		reader = dbcmd.ExecuteReader(); // execute command which returns a reader
	}

	public void InsertGPSPosition(string tableName, ArrayList values){
		string query = string.Format("INSERT INTO {0} VALUES ( {1}, {2}, {3}, {4}, '{5}')", 
		                             tableName, values[0], values[1], values[2], values[3], values[4]);
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
	}

	public ArrayList SingleSelectWhere(string tableName, string itemToSelect,
		string wCol, string wPar, string wValue){ // Selects a single Item
		string query = "SELECT " + itemToSelect + " FROM " + tableName + " WHERE " + wCol + wPar + wValue;
		dbcmd = dbcon.CreateCommand();
		dbcmd.CommandText = query;
		reader = dbcmd.ExecuteReader();
		ArrayList readArray = new ArrayList();
		while(reader.Read()){
			readArray.Add(reader.GetString(0)); // Fill array with all matches
		}
		return readArray; // return matches
	}

	public void CloseDB(){
		reader.Close(); // clean everything up
		reader = null;
		dbcmd.Dispose();
		dbcmd = null;
		dbcon.Close();
		dbcon = null;
	}
}