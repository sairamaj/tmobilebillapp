using System;
using Microsoft.WindowsAzure.Storage.Table;

namespace SelfService.Server.Models
{
    public class StudentAttendanceEntity : TableEntity
    {
        public string Name => this.RowKey;
        public string ClassId => this.PartitionKey;
        public DateTime DateTime { get; set; }
    }
}