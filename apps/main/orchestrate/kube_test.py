from kubernetes import client, config, watch
from kubernetes.client import Configuration, ApiClient

DEV_KUBE_CONFIG = {
    "apiVersion": "v1",
    "clusters": [
        {
            "cluster": {
                "server": "https://10.4.2.54:6443",
                "certificate-authority-data": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURHakNDQWdLZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREErTVNjd0ZBWURWUVFLRXcxaGJHbGkKWVdKaElHTnNiM1ZrTUE4R0ExVUVDaE1JYUdGdVozcG9iM1V4RXpBUkJnTlZCQU1UQ210MVltVnlibVYwWlhNdwpIaGNOTWpBd056RXpNRGt4T1RNeVdoY05NekF3TnpFeE1Ea3hPVE15V2pBK01TY3dGQVlEVlFRS0V3MWhiR2xpCllXSmhJR05zYjNWa01BOEdBMVVFQ2hNSWFHRnVaM3BvYjNVeEV6QVJCZ05WQkFNVENtdDFZbVZ5Ym1WMFpYTXcKZ2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXdnZ0VLQW9JQkFRQ3BlQnVTNEFlMTFxM1FES3dpdVlnWAprSy9OTVBvNkhMYUNwaVNIWWNaOS9kdUdlcGJKemRheHFsaDN1Zzg1dG1HWmxQTWI3NW1YbXRUN3dXNWc5NDRjCjc1ZWVNTFZTL2lXV1FqVnZnaU5GWWRPY3lrNHBaZnN4bUJtL2NaUytxMmYvM0IxM3NoRms0S3RlRkxYZWNRZFEKMkRMZjdBcnNwdmtFQktHZjNaazNzTE42dGkvdXdKb010bHB4OTg5M2tYL1VFYUpIV0hMRThqWWlLUEc1Tk9PZApKbER2cy9LMzArMk9yWHBkVTVGRG5xT2lxaXE2SnpLVTQwVVpwV2FrbzdtUHhWWWxIM05JcHhXbUZCcWVGOXAvCkdXcDVFcmxldTFuV3N3R3NINDg4MWxZYW95aTBTbVhhbnk2djRzbU5CQitYcFV2TTFCNldWMlozaGRSQnFrMW4KQWdNQkFBR2pJekFoTUE0R0ExVWREd0VCL3dRRUF3SUNwREFQQmdOVkhSTUJBZjhFQlRBREFRSC9NQTBHQ1NxRwpTSWIzRFFFQkN3VUFBNElCQVFCNmZIRklVdHF0cFd2K1p2emE4MkJ2YktCTm0rMFhlVDR3ZHdFMTNobm5TSFUyCm40c2hjR1F2Y2hidDFHV0lCNlcyNWEvNWdXVEtKZHIrcnV5N0tLT1N2eU16MmVtd2pkUWNoRFRHYjA1cTVidE0KK1JudXUvT0dqNDZlK0xPL0hDbU1Gd3lDOEQwdGpBRFlqdGR6MUNIbitvNnhtQ2NOOTV6ajNabGpacFFqd1VKbQpOdDlCQU5MN0QwekRKckN2RnBtS00vWXpFR0lNUldROWZXcnZHMFYvV2c2K0tVNTlzcGpYU1hzZFQwNElXckRZCmZyc1RhbFdtcHNYTnBXV0p6UHVJQThYSy9zTDFLVkp3QnB0Vko1dnpIeWgzN1UyTVkrdnF4Q1poOGZ5V1BwUDcKU09WMGF4QkhxQllSZHd5NEZ2VkkwUDNveVRzdkNjN0NEazdYNHQvQQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="
            },
            "name": "kubernetes"
        }
    ],
    "contexts": [
        {
            "context": {
                "cluster": "kubernetes",
                "user": "kubernetes-admin"
            },
            "name": "kubernetes-admin-c52cb6ad200314d608c83bc5c5edce7bd"
        }
    ],
    "current-context": "kubernetes-admin-c52cb6ad200314d608c83bc5c5edce7bd",
    "kind": "Config",
    "preferences": {},
    "users": [
        {
            "name": "kubernetes-admin",
            "user": {
                "client-certificate-data": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMxakNDQWorZ0F3SUJBZ0lER09QQU1BMEdDU3FHU0liM0RRRUJDd1VBTUdveEtqQW9CZ05WQkFvVElXTTEKTW1OaU5tRmtNakF3TXpFMFpEWXdPR000TTJKak5XTTFaV1JqWlRkaVpERVFNQTRHQTFVRUN4TUhaR1ZtWVhWcwpkREVxTUNnR0ExVUVBeE1oWXpVeVkySTJZV1F5TURBek1UUmtOakE0WXpnelltTTFZelZsWkdObE4ySmtNQjRYCkRUSXdNRGN4TXpBNU1qQXdNRm9YRFRJek1EY3hNekE1TWpVeE1Wb3dTREVWTUJNR0ExVUVDaE1NYzNsemRHVnQKT25WelpYSnpNUWt3QndZRFZRUUxFd0F4SkRBaUJnTlZCQU1UR3pFNE1qQTJPVEV3TnpjM01USTBNalV0TVRVNQpORFl6TWpNeE1UQ0JuekFOQmdrcWhraUc5dzBCQVFFRkFBT0JqUUF3Z1lrQ2dZRUE0NXFLOUVlVGZML216ekp4CnZKb1NwS0t4V1pqN1Bwd29FTEppdlgwdy9RN2E3QXNJdkFoWGcwSzJ6bFBOS3dBUXREeVU5MktIaml4OGROekkKL1YwOUNyUzZzR2lLOWVDWHNHUDh1TG5FbjRnYmR2KzU2cDk5VXlRa1hkZDE1UGRQMWMrVVIrblVUQnY5OTMwbgplb0NkMGNhRm1WYS9EWGtGZWtpbHpuTk51TzBDQXdFQUFhT0JxekNCcURBT0JnTlZIUThCQWY4RUJBTUNCNEF3CkV3WURWUjBsQkF3d0NnWUlLd1lCQlFVSEF3SXdEQVlEVlIwVEFRSC9CQUl3QURBOEJnZ3JCZ0VGQlFjQkFRUXcKTUM0d0xBWUlLd1lCQlFVSE1BR0dJR2gwZEhBNkx5OWpaWEowY3k1aFkzTXVZV3hwZVhWdUxtTnZiUzl2WTNOdwpNRFVHQTFVZEh3UXVNQ3d3S3FBb29DYUdKR2gwZEhBNkx5OWpaWEowY3k1aFkzTXVZV3hwZVhWdUxtTnZiUzl5CmIyOTBMbU55YkRBTkJna3Foa2lHOXcwQkFRc0ZBQU9CZ1FCclhKZmlSWDBJRGgxN3RiTUpNZFB1clFaWWZ4bGsKaXlHNFpsTGR5VGovQjRScGJkeThlZXM5S25xVFh4QVRPYmdLZkhKemx1MHhSY3crOUdKVzFtM0RGcFRFOWdBWgpvNFpPRm1TZE1mQW1GNFN6aVpjbmY3S3V0aU52ck82T2tkdTdrQWozaUhqVUhYWXczd21iSi9FVzBrOUl6SlpECnVLdmNWWldveDBBcjNRPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQotLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS0KTUlJQy96Q0NBbWlnQXdJQkFnSURHT091TUEwR0NTcUdTSWIzRFFFQkN3VUFNR0l4Q3pBSkJnTlZCQVlUQWtOTwpNUkV3RHdZRFZRUUlEQWhhYUdWS2FXRnVaekVSTUE4R0ExVUVCd3dJU0dGdVoxcG9iM1V4RURBT0JnTlZCQW9NCkIwRnNhV0poWW1FeEREQUtCZ05WQkFzTUEwRkRVekVOTUFzR0ExVUVBd3dFY205dmREQWVGdzB5TURBM01UTXcKT1RFek1EQmFGdzAwTURBM01EZ3dPVEU0TURCYU1Hb3hLakFvQmdOVkJBb1RJV00xTW1OaU5tRmtNakF3TXpFMApaRFl3T0dNNE0ySmpOV00xWldSalpUZGlaREVRTUE0R0ExVUVDeE1IWkdWbVlYVnNkREVxTUNnR0ExVUVBeE1oCll6VXlZMkkyWVdReU1EQXpNVFJrTmpBNFl6Z3pZbU0xWXpWbFpHTmxOMkprTUlHZk1BMEdDU3FHU0liM0RRRUIKQVFVQUE0R05BRENCaVFLQmdRQ3pFNGFyeElrVGt0N1dGOThCZXVPUTN6cmhNVEJYODBiZEpXUVdyVmgxOGtOWQppWUdQcnNQNjNscGlUZWVBcHZUNERSakgvSUFVaUkrTmZlcVdpRGk1VHl4a0dLYkNUQkVPUTJZQmFiUlJWU2ZPCndycHcrNzRLN0J4YkY1S21SQVBhSVRwOFh6OGJFMDIvUno2RE5TYVh3VHcrNC9iOGdZNXJGeDBWNWlVYi93SUQKQVFBQm80RzZNSUczTUE0R0ExVWREd0VCL3dRRUF3SUNyREFQQmdOVkhSTUJBZjhFQlRBREFRSC9NQjhHQTFVZApJd1FZTUJhQUZJVmEvOTBqelNWdldFRnZubTFGT1p0WWZYWC9NRHdHQ0NzR0FRVUZCd0VCQkRBd0xqQXNCZ2dyCkJnRUZCUWN3QVlZZ2FIUjBjRG92TDJObGNuUnpMbUZqY3k1aGJHbDVkVzR1WTI5dEwyOWpjM0F3TlFZRFZSMGYKQkM0d0xEQXFvQ2lnSm9Za2FIUjBjRG92TDJObGNuUnpMbUZqY3k1aGJHbDVkVzR1WTI5dEwzSnZiM1F1WTNKcwpNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0R0JBRTlXc2luZHdjUmFLRmlFRFhTWmYxZmlVcE14T29LZmJUa1FxYzNBCk5icHJyL05TZ1RPSVN2MXdWWXdzTG5sQ3BBZVJSblBhb0FCL0oyeFRMQy9IeVZUcXAwQWFYcTVrNEdNbGkrMSsKTXdudTA2R0U1RmU1Q1lWamR6R0Vqb3AwK1Z5SEk5R0VFZnEvTS9SenFBMG9PUDEyS2Q5UlQwc3pSY1ZGWU1GSwp5NHRzCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",
                "client-key-data": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDV3dJQkFBS0JnUURqbW9yMFI1Tjh2K2JQTW5HOG1oS2tvckZabVBzK25DZ1FzbUs5ZlREOUR0cnNDd2k4CkNGZURRcmJPVTgwckFCQzBQSlQzWW9lT0xIeDAzTWo5WFQwS3RMcXdhSXIxNEpld1kveTR1Y1NmaUJ0Mi83bnEKbjMxVEpDUmQxM1hrOTAvVno1Ukg2ZFJNRy8zM2ZTZDZnSjNSeG9XWlZyOE5lUVY2U0tYT2MwMjQ3UUlEQVFBQgpBb0dBUGpoMVhDcGxDMmw2czVIYXZmQnd3RWtwcXBERHZtMzZGZlp1UDljRm1XaUNPSjBibWl1OW9NaVFLUCtICnl3V05pM2cwVVJ6Q2FmK0hWbnMxQnU2Q1RQTGk3U3JLc3l6K3BRY29lNWlOeUVidzh1SVdTcWU2eXhVTm03UFUKMlArcEZjSFhGZkVxVDAvL01IaUsvTms1NXl5dTRYb0RYQTR6NEhKWjdCTTRIQkVDUVFEbzBqNjRTVExyNzFSegpLYnN1emZaSk55UmxNSEFYOEN1Y2NQTUQ4b3RDK09LVWIrZ0Vpd25TSm9ZVkR4K2IySDZqem9TVU5OUDhZNWRaCjFNbUhDZVBuQWtFQStrTlNIVEtIc0k4dWlJeitHWDFzRkMzYkd1Ukp6ZFVFR0lYM3dGdXNMRGpzVko4WFAwMTcKUy9wTkhkdVVLUmJ2N3dSaHZGcnRZL0V1TzIybDZmbmlDd0pBTE9POHJCT1ErZVNmUjhVWURpSXdCbFhYY3BzdwpRYTFRKzB6Ynpqc0psdFFkKzdqSDUzaFhZR21GR0xKZHlkS29PRFV0WXRYOHVZRUtRWXZCZjRQc3FRSkFJRkUzCk5sd0RGN0sxc0o1OFpiQkRsNnVBUXMyK0ZoMXU1UGZQMFlCRkVJVGRSK1F2YlZaRkdMK2UyNzh5TjhnbGZia1UKSWUyZ0FDcng3R3l4WXpDSWx3SkFWQXBJK3VxU1BaeVBXODJSYndlTjVrYVVSaEt0MmVtZmIyU2drM0pDcmp3VQpPVWI0SUphejF3dDBQb0MzNHVDeElqdjRoUW9ZZ1A1ZlZnR3lXL21oS0E9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo="
            }
        }
    ]
}

QA_KUBE_CONFIG = {
    "apiVersion": "v1",
    "clusters": [
        {
            "cluster": {
                "server": "https://10.6.2.182:6443",
                "certificate-authority-data": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURHakNDQWdLZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREErTVNjd0ZBWURWUVFLRXcxaGJHbGkKWVdKaElHTnNiM1ZrTUE4R0ExVUVDaE1JYUdGdVozcG9iM1V4RXpBUkJnTlZCQU1UQ210MVltVnlibVYwWlhNdwpIaGNOTWpBd09UQXpNRFl5TWpVeVdoY05NekF3T1RBeE1EWXlNalV5V2pBK01TY3dGQVlEVlFRS0V3MWhiR2xpCllXSmhJR05zYjNWa01BOEdBMVVFQ2hNSWFHRnVaM3BvYjNVeEV6QVJCZ05WQkFNVENtdDFZbVZ5Ym1WMFpYTXcKZ2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXdnZ0VLQW9JQkFRQ3JpanVnblY3MEF0dzRvNmo0SnExUApFUzZNdkRGR3VFcUhkUmxCRWNyemZ5RWFRL3VUbG4rVzJWSEMwVG1ob0taUmU3K3R3bzhHeUg4OGhJZEcxbldmCmVRZGZaSHRXakNqQ2p3cDRHdyt0aHpZWlc4U3pXdXBBRFRqUDVsL3VOc0VJdXdXNmtZWFI4cjRLdHBXcnI4bnUKcGYrSlZlcXhXSXFQandpSW1iQ1VWMzNTR2xVb3Bmdk5kZExvR3hJWEtjMnh6ekhwclRTT0ViRi8zeWtXc3U2cQovSjVFUXBoditKUHZDYjF4TXppT3NGc0NGNmRadXJTUlptak9YNm9vOUZEYlI1VEdadUNjY2xuZThySVVTVE5iClN4cUpncG5rRzBYNWlxS3h6Nll5S3hFTndXenRPbW5kYlVRK0RPZ00xd1U3NDgrWjc2TGhZVkIrNWo2MzF0c3QKQWdNQkFBR2pJekFoTUE0R0ExVWREd0VCL3dRRUF3SUNwREFQQmdOVkhSTUJBZjhFQlRBREFRSC9NQTBHQ1NxRwpTSWIzRFFFQkN3VUFBNElCQVFDVXJFRjhmdjJmdHluUzY3RnFrdllPSzkxWUpicnRVcTRCZmd3SExOaEIwRnczCnR5dUc2WEhOb0o5TEovanZra1Uwc1RtdHJOU21FNlNudHZvK1hLd0lvWDdRc1VQOWZzM3BiUVMrNExmWGh5cngKNFhSb2xqbEJuNXNIbWRLNUJWbzI3bmx2VEtGZjRCZXdWK25PZURuUEJFVzNCa2F0VUpla1kvTWhYRDFSWHl2MApzcGNZcVNIY0w2RXdrYURWT3BJK3BkU1BLOEQwbmF1VHpLV1MzL3VaSkFKVHhGVDdNS0NsYmZuVjA4N3p4cndaClNtNHBuL2JBcUpzZnF0T09qZWp0K2xMMGpoY0dKTk9PY3o5b1dPUmpBV0NRWTJsWllsbXE5VjJKMGdoS1VFc0wKRHNQMU1kcHg5bEV1WTVmWEFrUFFXdXFzRzlPUVdhL0VVeFlaeGQ4TwotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="
            },
            "name": "kubernetes"
        }
    ],
    "contexts": [
        {
            "context": {
                "cluster": "kubernetes",
                "user": "kubernetes-admin"
            },
            "name": "kubernetes-admin-c5af3042e70684dc7abac02e2340c2188"
        }
    ],
    "current-context": "kubernetes-admin-c5af3042e70684dc7abac02e2340c2188",
    "kind": "Config",
    "preferences": {},
    "users": [
        {
            "name": "kubernetes-admin",
            "user": {
                "client-certificate-data": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMxakNDQWorZ0F3SUJBZ0lER2dOaU1BMEdDU3FHU0liM0RRRUJDd1VBTUdveEtqQW9CZ05WQkFvVElXTTEKWVdZek1EUXlaVGN3TmpnMFpHTTNZV0poWXpBeVpUSXpOREJqTWpFNE9ERVFNQTRHQTFVRUN4TUhaR1ZtWVhWcwpkREVxTUNnR0ExVUVBeE1oWXpWaFpqTXdOREpsTnpBMk9EUmtZemRoWW1Gak1ESmxNak0wTUdNeU1UZzRNQjRYCkRUSXdNRGt3TXpBMk1qTXdNRm9YRFRJek1Ea3dNekEyTWpnMU5sb3dTREVWTUJNR0ExVUVDaE1NYzNsemRHVnQKT25WelpYSnpNUWt3QndZRFZRUUxFd0F4SkRBaUJnTlZCQU1UR3pFNE1qQTJPVEV3TnpjM01USTBNalV0TVRVNQpPVEV4TkRVek5qQ0JuekFOQmdrcWhraUc5dzBCQVFFRkFBT0JqUUF3Z1lrQ2dZRUF1blJ2UTdqTm1DRXNDZ011Cm52VnBTckRacjNEeFFBS2FoNHY0aVJ5U3ZnMDZESHZYQjc5RW1JVXN2RmpIMGRBbHpxR000aTBmUUJjMUVFREgKUjcxYUZuYncyYVV1VkIxY3FHMk9Oa3lSc3RTR3kvclpxOUVzdzdGZXhBQ3EyRUJIUFVyeUsvaXZId1NmcldIQQprZkozUWJZYTNZSXpQZ1pud25xUWxiQ0J4ZFVDQXdFQUFhT0JxekNCcURBT0JnTlZIUThCQWY4RUJBTUNCNEF3CkV3WURWUjBsQkF3d0NnWUlLd1lCQlFVSEF3SXdEQVlEVlIwVEFRSC9CQUl3QURBOEJnZ3JCZ0VGQlFjQkFRUXcKTUM0d0xBWUlLd1lCQlFVSE1BR0dJR2gwZEhBNkx5OWpaWEowY3k1aFkzTXVZV3hwZVhWdUxtTnZiUzl2WTNOdwpNRFVHQTFVZEh3UXVNQ3d3S3FBb29DYUdKR2gwZEhBNkx5OWpaWEowY3k1aFkzTXVZV3hwZVhWdUxtTnZiUzl5CmIyOTBMbU55YkRBTkJna3Foa2lHOXcwQkFRc0ZBQU9CZ1FBYzRTVjhiNjdERzZTaXNPZ2pJRlFSUS9ROFpXcloKN1ExcjlXdWZuQ0syR0Z3bmhrUXJVNVFFWDVSR2FYUkx3ZkFBeG5JMTNhSnZJN2tvdlJXVjdJaFJoVzRlYzBadApLaGRtVXIrVHJYK0RIUlpsNzgzcDBCS0pHUDRVRCtzaVF4RzNjNEdOaUdUdUZOVld6UXoyK1hZcDB5RW83eXJSCll3UDMzTTVDSUNVSHFRPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQotLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS0KTUlJQy96Q0NBbWlnQXdJQkFnSURHZ05ETUEwR0NTcUdTSWIzRFFFQkN3VUFNR0l4Q3pBSkJnTlZCQVlUQWtOTwpNUkV3RHdZRFZRUUlEQWhhYUdWS2FXRnVaekVSTUE4R0ExVUVCd3dJU0dGdVoxcG9iM1V4RURBT0JnTlZCQW9NCkIwRnNhV0poWW1FeEREQUtCZ05WQkFzTUEwRkRVekVOTUFzR0ExVUVBd3dFY205dmREQWVGdzB5TURBNU1ETXcKTmpFMk1EQmFGdzAwTURBNE1qa3dOakl4TWpGYU1Hb3hLakFvQmdOVkJBb1RJV00xWVdZek1EUXlaVGN3TmpnMApaR00zWVdKaFl6QXlaVEl6TkRCak1qRTRPREVRTUE0R0ExVUVDeE1IWkdWbVlYVnNkREVxTUNnR0ExVUVBeE1oCll6Vmhaak13TkRKbE56QTJPRFJrWXpkaFltRmpNREpsTWpNME1HTXlNVGc0TUlHZk1BMEdDU3FHU0liM0RRRUIKQVFVQUE0R05BRENCaVFLQmdRQzNxOEl6SjdLdHg3S3hyRHVxLzgyaWlzd1J5NnpPSVY5RWxLZlV2VHFsdHlXMgphSjVmRmhVeEdSb2ZIbWFFeXBsM2RMMkxJUEFBVTV2YlFJSHlWUjN1VkpuK0wrSFppOHd3VlJYeWpqbTNheUhTCklEcEgvZndjY0czSk5DNUw2aDRmWEJEcThVaGpENkdLZGpINnU4RnBPQi94YlNJQkF4dEFQYS8vUjBYbzV3SUQKQVFBQm80RzZNSUczTUE0R0ExVWREd0VCL3dRRUF3SUNyREFQQmdOVkhSTUJBZjhFQlRBREFRSC9NQjhHQTFVZApJd1FZTUJhQUZJVmEvOTBqelNWdldFRnZubTFGT1p0WWZYWC9NRHdHQ0NzR0FRVUZCd0VCQkRBd0xqQXNCZ2dyCkJnRUZCUWN3QVlZZ2FIUjBjRG92TDJObGNuUnpMbUZqY3k1aGJHbDVkVzR1WTI5dEwyOWpjM0F3TlFZRFZSMGYKQkM0d0xEQXFvQ2lnSm9Za2FIUjBjRG92TDJObGNuUnpMbUZqY3k1aGJHbDVkVzR1WTI5dEwzSnZiM1F1WTNKcwpNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0R0JBTUd1TGc2NkFmdEMxaTR5TUlONXNocHFmdDFNZnY3WCtNbjcrUUZkCnhOV2tsNGlOcDZ6Znd6V2xHbENmTmV2VE5oMHhtU0E2R29XWGJkdllkZ1Rrb1BsQ2o4OVBqTVhjc1VVVEpFVEQKdDhpbU1IOEdrQWQ0Z2cyNWgxMjlJR0dYZkhyWmo0QUwrdUtTSU4rc0xrVDd3d0RPcHFBY0huenprUkFJSFdOYQpHZHY1Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K",
                "client-key-data": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWHdJQkFBS0JnUUM2ZEc5RHVNMllJU3dLQXk2ZTlXbEtzTm12Y1BGQUFwcUhpL2lKSEpLK0RUb01lOWNICnYwU1loU3k4V01mUjBDWE9vWXppTFI5QUZ6VVFRTWRIdlZvV2R2RFpwUzVVSFZ5b2JZNDJUSkd5MUliTCt0bXIKMFN6RHNWN0VBS3JZUUVjOVN2SXIrSzhmQkordFljQ1I4bmRCdGhyZGdqTStCbWZDZXBDVnNJSEYxUUlEQVFBQgpBb0dCQUlqTU1uSDZYWVUzR1V1RFNDcENIZTA1MFl6QmpZOE1HZnBHL0tNRVBybUhsTVpoK2NMcVZ0YWNKdFZOClFkV3pKSG4wMXh0K1JZWk5RSlpiSUpxRzExZVJLZWxFL292VXZTUDYrbW1JQWxCa2luSHB0emlMS2pVaXJjaFAKN2ZXUXIrTmx1OFp3T3ltQmRDUzVVS1lWMCs2bXRVc2pzTHoyT3laNDNwRUd3QlJCQWtFQTVESTg2eW5heVV1MAozaitVRWZsQi9JTEptVlF5WFhBUjVTUzJ2N3dlTGV6WDI0Rzh1aVRSNjQvUEVnQUcvSFFtZitRZElBclp3VDFXCjRCZGNGMFBBNVFKQkFORXNPUmpFUVZmNnh5VXgrZjZ3Y0pnblU3K3NLelpGZUVGVTFRbW43MEw0ZXRHckhieTUKWTU3NTdwc3l4bkNKUXRkV2xkUG9qVXJ4R05iNkNaZzIwakVDUVFDa0J3aUs4VGIyNHBoTCtOOXlXL3oyaVB4bwpYb0VsY04wc0hNdlAzbVRERmkvQzlPcTMwcWVoNzJra3d5aENaeXNWV3Q4a25TZ1JJd3BEWWdjc0llT1JBa0VBCmxIVWdxUlZSazFIbjJkeFlwSTB4dkt2YzR1TWRZRTE2QmxSaFI1TXJXNHJrRUwrMFFXZ0s3cUJRMjFIMFNaY0MKRzdmV2F5cFliZUlrVVIveGcxa1ZZUUpCQUlKUnpNOFg1blp6Y3AvcENsTEVwTDNBK0NPYWJJR1RyRHREUTdQdQpxcWYwNDhGL09VbHpLMkUvMy9LWWdxbEN2ZUVBbUszbGZGNXh0ZDVOUVFGMHkyMD0KLS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0K"
            }
        }
    ]
}


def get_pods():
    v1 = client.CoreV1Api()
    for pod in v1.list_namespaced_pod('default').items:
        print(pod.metadata.name)
    pass


def list_pod(cli, namespace: str='default'):
    for pod in cli.list_namespaced_pod(namespace=namespace).items:
        print(pod.metadata.name)


def new_client_from_dict(conf: dict, context: str):
    client_config = type.__call__(Configuration)
    config.load_kube_config_from_dict(config_dict=conf, context=context, persist_config=False,
                                      client_configuration=client_config)
    return ApiClient(configuration=client_config)


def multi_client():
    # client1 = client.CoreV1Api(api_client=config.new_client_from_config(config_file=DEV_KUBE_CONFIG, context='kubernetes-admin-c52cb6ad200314d608c83bc5c5edce7bd'))
    # client2 = client.CoreV1Api(api_client=config.new_client_from_config(config_file=QA_KUBE_CONFIG, context='kubernetes-admin-c5af3042e70684dc7abac02e2340c2188'))
    client1 = client.CoreV1Api(api_client=new_client_from_dict(DEV_KUBE_CONFIG, context='kubernetes-admin-c52cb6ad200314d608c83bc5c5edce7bd'))
    client2 = client.CoreV1Api(api_client=new_client_from_dict(QA_KUBE_CONFIG, context='kubernetes-admin-c5af3042e70684dc7abac02e2340c2188'))

    list_pod(client1)
    list_pod(client2)


def test():
    config.load_kube_config_from_dict(config_dict=DEV_KUBE_CONFIG,
                                      context='kubernetes-admin-c52cb6ad200314d608c83bc5c5edce7bd')

    v1 = client.CoreV1Api()
    print('v1')
    for pod in v1.list_namespaced_pod('default').items:
        print(pod.metadata.name)

    config.load_kube_config_from_dict(config_dict=QA_KUBE_CONFIG,
                                      context='kubernetes-admin-c5af3042e70684dc7abac02e2340c2188')

    v2 = client.CoreV1Api()
    print('v2')
    for pod in v2.list_namespaced_pod('default').items:
        print(pod.metadata.name)

    print('v1')
    for pod in v1.list_namespaced_pod('default').items:
        print(pod.metadata.name)


def watch_namespace():
    client1 = client.CoreV1Api(
    api_client=new_client_from_dict(DEV_KUBE_CONFIG, context='kubernetes-admin-c52cb6ad200314d608c83bc5c5edce7bd'))
    w = watch.Watch()
    count = 10
    for event in w.stream(client1.list_namespaced_pod, namespace='default', _request_timeout=60):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        count -= 1
        if not count:
            w.stop()


if __name__ == '__main__':
    # multi_client()
    watch_namespace()