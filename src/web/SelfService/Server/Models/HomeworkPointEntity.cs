using Microsoft.WindowsAzure.Storage.Table;

namespace SelfService.Server.Models
{
    public class HomeworkPointEntity : TableEntity
    {
        public HomeworkPointEntity()
        {
            this.PartitionKey = "homeworkpoint";
        }
        public string Id
        {
            get => RowKey;
            set
            {
                this.RowKey = value;
            }
        }

        public int NumberId {get; set;}
        public string Description { get; set; }
        public string Category { get; set; }
        public int NumberofPoints { get; set; }
    }
}