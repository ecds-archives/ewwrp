<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:eg="http://www.tei-c.org/ns/Examples"
	xmlns:tei="http://www.tei-c.org/ns/1.0" 
	xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" 
	xmlns:exsl="http://exslt.org/common"
	xmlns:msxsl="urn:schemas-microsoft-com:xslt"
	xmlns:fn="http://www.w3.org/2005/xpath-functions"
	extension-element-prefixes="exsl msxsl"
	xmlns="http://www.w3.org/1999/xhtml" 
	exclude-result-prefixes="xsl tei xd eg fn #default">
	<xd:doc  scope="stylesheet">
		<xd:desc>
			<xd:p><xd:b>Created on:</xd:b> Nov 17, 2011</xd:p>
			<xd:p><xd:b>Author:</xd:b> John A. Walsh</xd:p>
			<xd:p>TEI Boilerplate stylesheet: Copies TEI document, with a very few modifications
				into an html shell, which provides access to javascript and other features from the
				html/browser environment.</xd:p>
		</xd:desc>
	</xd:doc>

	<xsl:output encoding="UTF-8" method="xml" omit-xml-declaration="yes"/>
	
	<xsl:param name="teibpHome" select="'http://dcl.slis.indiana.edu/teibp/'"/>
	
	<!-- special characters -->
	<xsl:param name="quot"><text>"</text></xsl:param>
	<xsl:param name="apos"><text>'</text></xsl:param>
	
	<!-- interface text -->
	<xsl:param name="pbNote"><text>page: </text></xsl:param>
	<xsl:param name="altTextPbFacs"><text>view page image(s)</text></xsl:param>
	<xsl:param name="pathToImages">/wp-content/plugins/teipluswp/images/</xsl:param>
	
	<!-- parameters for file paths or URLs -->
	<!-- modify filePrefix to point to files on your own server, 
		or to specify a relatie path, e.g.:
		<xsl:param name="filePrefix" select="'http://dcl.slis.indiana.edu/teibp'"/>
		
	-->
	<xsl:param name="filePrefix" select="'..'"/>
	
	<xd:doc xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl">
		<xd:desc>
			<xd:p>Match document root and create and html5 wrapper for the TEI document, which is
				copied, with some modification, into the HTML document.</xd:p>
		</xd:desc>
	</xd:doc>

	<xsl:key name="ids" match="//*" use="@xml:id"/>
	
	<xsl:template match="@*">
		<!-- copy select elements -->
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="*">
		<xsl:element name="{local-name()}">
			<xsl:call-template name="addID"/>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template name="rendition">
		<xsl:if test="@rendition">
			<xsl:attribute name="rendition">
				<xsl:value-of select="@rendition"/>
			</xsl:attribute>
		</xsl:if>
	</xsl:template>

	<xsl:template match="@xml:id">
		<!-- @xml:id is copied to @id, which browsers can use
			for internal links.
		-->
		<!--
		<xsl:attribute name="xml:id">
			<xsl:value-of select="."/>
		</xsl:attribute>
		-->
		<xsl:attribute name="id">
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>

	<xsl:template match="tei:ref[@target]" priority="99">
		<a href="{@target}">
			<xsl:call-template name="rendition"/>
			<xsl:apply-templates/>
		</a>
	</xsl:template>

	<xsl:template match="tei:figure[tei:graphic[@url]]" priority="99">
		<xsl:copy>
			<xsl:apply-templates select="@*"/>
			<xsl:call-template name="addID"/>
			<figure>
			  <img alt="{normalize-space(tei:figDesc)}">
			    <xsl:attribute name="src">
			      <xsl:value-of select="$pathToImages"/>
			      <xsl:value-of select="tei:graphic/@url"/>
			    </xsl:attribute>
			  </img>
			  <center>
			    <xsl:apply-templates select="*[local-name() != 'graphic' and local-name() != 'figDesc']"/>
			  </center>
			</figure>
		</xsl:copy>
	</xsl:template>
	
	<xsl:template name="addID">
		<xsl:if test="not(ancestor::eg:egXML)">
			<xsl:attribute name="id">
				<xsl:choose>
				<xsl:when test="@xml:id">
					<xsl:value-of select="@xml:id"/>
				</xsl:when>
				<xsl:otherwise>
				<xsl:call-template name="generate-unique-id">
					<xsl:with-param name="root" select="generate-id()"/>
				</xsl:call-template>
				</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
		</xsl:if>
	</xsl:template>
    
	<xsl:template name="generate-unique-id">
		<xsl:param name="root"/>
		<xsl:param name="suffix"/>
		<xsl:variable name="id" select="concat($root,$suffix)"/>
		<xsl:choose>
			<xsl:when test="key('ids',$id)">
				<!--
				<xsl:message>
					<xsl:value-of select="concat('Found duplicate id: ',$id)"/>
				</xsl:message>
				-->
				<xsl:call-template name="generate-unique-id">
					<xsl:with-param name="root" select="$root"/>
					<xsl:with-param name="suffix" select="concat($suffix,'f')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$id"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
    
	<xsl:variable name="htmlFooter">
		<footer>Powered by <a href="{$teibpHome}">TEI Boilerplate</a>. TEI Boilerplate is licensed under a <a
				href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0
				Unported License</a>. <a href="http://creativecommons.org/licenses/by/3.0/"><img
					alt="Creative Commons License" style="border-width:0;"
					src="http://i.creativecommons.org/l/by/3.0/80x15.png"/></a>
		</footer>
	</xsl:variable>
	
	<xsl:template match="tei:pb">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
	</xsl:template>

	<xsl:template match="eg:egXML">
		<xsl:element name="{local-name()}">
			<xsl:apply-templates select="@*"/>
			<xsl:call-template name="addID"/>
			<xsl:call-template name="xml-to-string">
				<xsl:with-param name="node-set">
					<xsl:copy-of select="node()"/>
				</xsl:with-param>
			</xsl:call-template>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="eg:egXML//comment()">
		<xsl:comment><xsl:value-of select="."/></xsl:comment>
	</xsl:template>

	
</xsl:stylesheet>
