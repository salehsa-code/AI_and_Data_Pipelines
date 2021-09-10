<#
.SYNOPSIS
    PowerShell script to check which files are updated based on the when the pipline last ran successfully, and update variables accordingly"

.EXAMPLE


.NOTES
    -
#>

[CmdletBinding()]
param (
    $PersonalToken,
    $WorkingDirectory, #$(System.DefaultWorkingDirectory)
    $StagingDirectory #$(Build.StagingDirectory)
)


#Set variables 
$personalToken =  $PersonalToken
$workingDirectory = $WorkingDirectory
$stagingDirectory = $StagingDirectory
$targetfolder = $stagingDirectory  + "/"

#Get the changeSet/commit to check which files are updated

#Set authentication header -- OBS:Now personal token to test but should be updated to service principle 
$AzureDevOpsAuthenicationHeader = @{Authorization = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$($personalToken)")) }

#Url AppFramework Latest build with definition number 253, only master branch
$url = "https://dev.azure.com/GBI-ODL/AppFramework/_apis/build/latest/253?branchName=master&api-version=5.0-preview.1"

try {
    Write-Output "Get source version.."
    $response = (Invoke-RestMethod -Uri $url -Method GET -Headers $AzureDevOpsAuthenicationHeader -ContentType 'application/json')        
}
catch {       
        Write-Output "Something went wrong when trying to get lastest build from master.."
}

if($response){   
    Write-Output "Git diff to see which files are updated.."
    $editedFiles = (git diff HEAD $response.sourceVersion --name-only)
    if($editedFiles){
        Write-Output "Edited files: $($editedFiles)"
        Write-Host "##vso[task.setvariable variable=editedFiles;]$editedFiles"

        Write-Output "Set variables to true based on edited files.."
        $editedFiles = $editedFiles.Split(" ")

        $editedFiles | ForEach-Object {
            Switch -Wildcard ($_ ) {
                'source_schema/*' { 
                        Write-Host "Avro variable will be updated to true.."
                        Write-Host "##vso[task.setvariable variable=avroUpdate;]true" }
                'sql_ddls/*' {  
                        Write-Host "Sql variable will be updated to true.."
                        Write-Host "##vso[task.setvariable variable=sqlUpdate;]true" }
            }
        }

        foreach($editedFile in $editedFiles){
            if ($editedFile -match "source_schema" -or $editedFile -match "sql_ddls"){             
                Write-Output "Following matching path which will be added to target folder: $($editedFile)"
                
                #create a temp folder to hold the changed files
                $target = $targetfolder + "\" + $editedFile
                New-Item -Force $target
                $testpath = Test-Path -Path $workingDirectory\$editedFile
                #In case the file is dropped or deleted
                if ($testpath -eq 'true'){
                Copy-Item -Path $workingDirectory\$editedFile -Destination $target -Force
                }
                else {
                    Write-Output "File $($editedFile) was deleted and will not be added"
                }
            }else{
                Write-Output "Following path are not matching and will therefor not be added to target folder: $($editedFile)" 
            }
        }
    }else{ 
        Write-Output "No files are updated for following folders are updated since last successful build: source_schema/ & sql_ddls/"
    }
}else{
    Write-Output "No completed builds were found for pipeline with definitionId 253 to compare with.."
}