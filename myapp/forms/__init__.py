from wtforms import TextField, Form, validators, SelectField

class PersonForm(Form):
    first_name = TextField("First name", [validators.Length(min=2, max=50)])
    last_name = TextField("Last name", [validators.Length(min=2, max=50)])

class VideoForm(Form):
    title = TextField("Title")
    code = TextField("Code")
    actors = SelectField("Actors" , coerce=int)
    release_date = TextField("release_date")

class SceneForm(Form):
    summary = TextField("Summary")
    video = SelectField("Video", coerce=int)
    start_time = TextField("Start time")
    end_time = TextField("End time")
