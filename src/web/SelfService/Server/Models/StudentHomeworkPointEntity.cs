using System;
using System.Collections.Generic;
using Microsoft.WindowsAzure.Storage.Table;

namespace SelfService.Server.Models
{
    public class StudentHomeworkPointEntity : TableEntity
    {
        public string StudentId
        {
            get => this.RowKey;
            set
            {
                this.RowKey = value;
            }
        }

        public string HomeworkPointIds { get; set; }
    }
}