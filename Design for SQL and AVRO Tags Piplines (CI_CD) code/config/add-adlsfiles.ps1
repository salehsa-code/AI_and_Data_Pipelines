<#
.SYNOPSIS
    PowerShell script to add adls files based on update since last merge to master"

.EXAMPLE
    $Atenant = Tenant Id
    $AppKey = Client Secret 
    $WorkingDirectory = $(System.DefaultWorkingDirectory)
    $ArtifactPath

.NOTES
    -
#>

[CmdletBinding()]
param (
    $Atenant,
    $AppKey,
    #$ClientIdKey,
    $WorkingDirectory,
    $ArtifactPath,
    $AdlsAccountName
)

#Set variables 
$AadTenant = $Atenant
$AadAppKey = $AppKey
$AadAppId =  'ef8652e7-34d2-4d91-8fae-caa5271e83f5'
$WorkDir = $WorkingDirectory
$artPath = $ArtifactPath
$adlsAccountName = $AdlsAccountName
$FileSystemName = "odl1"

Write-Output 'Atenant' $AadTenant
Write-Output 'AadAppKey' $AadAppKey

#get updated files from artifact 
################################
#Set $path 

#Check if ADLS update has been done (meaning if package includes files for ADLS) - otherwise skip task..
#meaning if package - has a zip file name including combined or source_schema - continue

#Get OAuth2 Access Token from Azure AD
$body = @{
    "grant_type" = "client_credentials"
    "client_id" = "$AadAppId"
    "client_secret" = "$AadAppKey"
    "resource" = "https://storage.azure.com"
    "scope" = "https://storage.azure.com/.default"
}

$authResult = Invoke-RestMethod -Uri "https://login.microsoftonline.com/$AadTenant/oauth2/token" -Body $body -Method Post
#Make call to ADLS Gen2 to create directory path
$headers = @{
    "x-ms-version" = "2018-11-09"
    "Authorization" = "Bearer $($authResult.access_token)"
}




#"If-None-Match"= "*" # Add this to header if fail if the destination already exists, use a conditional request with If-None-Match: "*"


#Create URL for adding file
$url = "https://" + $adlsAccountName + ".dfs.core.windows.net/" + $FileSystemName + "/" + $path

Write-Output "URL to create directory path: $($url)"

Write-Output "Make call to ADLS Gen2 to create/update file.."
try {

    Write-Output "Make call to ADLS Gen2 to create/update $($path) file in following container: $($FileSystemName)"
    Invoke-RestMethod -Uri $url -Headers $headers -Method PUT -Verbose
    Write-Output "Update complete.."
}
catch
{       
    Write-Output "Something went wrong when trying to create/update file.."
}