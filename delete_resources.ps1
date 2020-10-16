Set-Variable -Name "subscription" -Value "5407d4ab-d915-4309-9a3f-339a90387e68"
Remove-AzResource -ResourceId "/subscriptions/$subscription/resourceGroups/rhr-qna/providers/Microsoft.Web/sites/rhr-qna-auth" -Force
Remove-AzResource -ResourceId "/subscriptions/$subscription/resourceGroups/rhr-qna/providers/Microsoft.Web/serverFarms/rhr-qna-auth" -Force
Remove-AzResource -ResourceId "/subscriptions/$subscription/resourceGroups/rhr-qna/providers/Microsoft.BotService/botServices/rhr-qna-auth" -Force

