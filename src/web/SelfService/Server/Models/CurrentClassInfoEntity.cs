using System;
using Microsoft.WindowsAzure.Storage.Table;

namespace SelfService.Server.Models
{
    public class CurrentClassInfoEntity : TableEntity
    {
        public DateTime DateTime { get; set; }
        public string ClassName { get; set; }
        public bool IsRunning {get; set;}
    }
}