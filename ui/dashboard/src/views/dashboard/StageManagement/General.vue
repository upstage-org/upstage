<template>
  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">Stage Name</label>
    </div>
    <div class="field-body">
      <div class="field">
        <p class="control is-expanded">
          <input class="input" type="text" placeholder="Full Name" />
        </p>
      </div>
      <div class="field">
        <p class="control is-expanded has-icons-right">
          <input class="input is-success" placeholder="Short Name" />
          <span class="icon is-small is-right">
            <i class="fas fa-check"></i>
          </span>
        </p>
        <p class="help">From which the stage URL is created</p>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">Description</label>
    </div>
    <div class="field-body">
      <div class="field">
        <div class="control">
          <textarea
            class="textarea"
            placeholder="enter a description (previously only for the splash screen that displays while loading - do we need 2 description fields now, one for the foyer display & one for the splash screen?)"
          ></textarea>
        </div>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">Media</label>
    </div>
    <div class="field-body">
      <div class="field is-narrow">
        <div class="control">
          <div class="select is-fullwidth">
            <select>
              <option>Media 1</option>
              <option>Media 2</option>
              <option>Media 3</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label">Users</label>
    </div>
    <div class="field-body">
      <div class="field is-narrow">
        <div class="control">
          <div class="select is-fullwidth">
            <select>
              <option>User 1</option>
              <option>User 2</option>
              <option>User 3</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label">
      <label class="label">Stage Status</label>
    </div>
    <div class="field-body">
      <div class="field is-narrow">
        <div class="control">
          <label class="radio">
            <input type="radio" name="status" />
            Live
          </label>
          <label class="radio">
            <input type="radio" name="status" />
            Upcoming
          </label>
          <label class="radio">
            <input type="radio" name="status" />
            Rehearsal
          </label>
        </div>
      </div>
    </div>
  </div>

  <div class="field is-horizontal">
    <div class="field-label">
      <!-- Left empty for spacing -->
    </div>
    <div class="field-body">
      <div class="field">
        <div class="control">
          <button class="button mr-2 mt-2 is-primary">Save Stage</button>
          <button class="button mr-2 mt-2 is-warning">Clear Chat</button>
          <button class="button mr-2 mt-2 is-warning">Sweep Stage</button>
          <button class="button mr-2 mt-2 is-dark">Hide From Stage List</button>
          <button class="button mr-2 mt-2 is-danger">Delete Stage</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
</style>