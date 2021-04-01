using System;

namespace SelfService.Shared
{
    public class HomeworkPoint
    {
        public string Id {get; set;}
        public string Category {get; set;}
        public string Description {get; set;}
        public int NumberofPoints {get; set;}
        public int NumberId {get; set;}


        public void Validate(){
            if( string.IsNullOrEmpty(this.Category)){
                throw new ArgumentException("Category required.");
            }
            if( string.IsNullOrEmpty(this.Description)){
                throw new ArgumentException("Description required.");
            }
            if( this.NumberofPoints <= 0){
                throw new ArgumentException($"Number of points cannot be zero or less than zero.");
            }
        }
    }
}