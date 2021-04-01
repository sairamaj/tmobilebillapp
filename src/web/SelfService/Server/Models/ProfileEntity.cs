using Microsoft.WindowsAzure.Storage.Table;

namespace SelfService.Server.Models
{
    public class ProfileEntity : TableEntity
    {
        public ProfileEntity()
        {
            this.PartitionKey = "profile";
        }
        
        public string Id {
            get => this.RowKey;
            set {
                this.RowKey = value;
            }
        }
        public string Name {get; set;}

        public string Location { get; set; }
        public string Phone { get; set; }
        public string Grade {get; set;}
        public string RegisteredClass {get; set;}
        public string GithubUrl { get; set; }
        public int HomeworkPoints {get; set;}
    }
}