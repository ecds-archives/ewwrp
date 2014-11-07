<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                xmlns:exist="http://exist.sourceforge.net/NS/exist"
                version="1.0">
    
    <xsl:variable name="figure-path">/Update/this/path/</xsl:variable>
    <xsl:variable name="figure-suffix">.jpg</xsl:variable>
    <xsl:variable name="thumbnail-path">/Update/this/path/</xsl:variable>
    <xsl:variable name="thumbnail-suffix">.gif</xsl:variable>
    
    <xsl:template match="tei:teiHeader" />
    
    <xsl:template match="exist:match">
        <span class="highlight"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="tei:figure" priority="99">
        <img>
            <xsl:attribute name="src"><xsl:copy-of select="$figure-path"/><xsl:value-of select="../@xml:id"/><xsl:copy-of select="$figure-suffix"/></xsl:attribute>
            <xsl:attribute name="alt"><xsl:value-of select="normalize-space(tei:figDesc)"/></xsl:attribute>
            <xsl:attribute name="title"><xsl:value-of select="normalize-space(tei:figDesc)"/></xsl:attribute>
        </img>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="tei:*">
        <div>
            <xsl:attribute name="class">tei-<xsl:value-of select="name(.)"/></xsl:attribute>
            <xsl:attribute name="rel">tei</xsl:attribute>
            <xsl:apply-templates/>
            <xsl:comment>This is necessary to prevent self-closing divs</xsl:comment>
        </div>
    </xsl:template>
    
</xsl:stylesheet>